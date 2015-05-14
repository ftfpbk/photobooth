#!/usr/bin/python
import threading
import time
import piggyphoto
import os, sys
import shutil
import pygame
from serial import Serial
from string import split,join
from pygame.locals import *
from templates import templates
from random import randrange
import Image, select, v4l2capture
from StringIO import StringIO


# set up serial port for button box and lens light
# and turn on all three buttons...
buttonpattern = [0, 1, 2, 4, 2, 1, 0, 4, 2, 1, 0, 1, 2, 4, 0, 2, 5, 2, 5, 7, 0, 7, 0, 7]
ser = Serial(port = '/dev/ttyACM0')
ser.write(str(7))

# list with raw image file suffixes, used for appending to files as they are created
suffix = [ 'a', 'b', 'c', 'd' ]

# execute a shell command, printing it to the console for useful for debugging purposes...
def shellcmd(command):
	print ' =>', command
	os.system(command)

# new filename generation function: returns next sequential filename
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename


# generate a composite image from a template, horizontal or vertical, abstracted 
#    and genericized so that various combinations of templates can be created...
def generate_composite(template, filename, blocking=True, generateprint=False):
	# base graphicsmagick commands to generate composites...
#	interrim = 'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 '
	interrim = templates[template][-2]
	ending = templates[template][-1]
	
	# generate interrim commands...
	for i in range(1,5):
		command = join(split(interrim, '&FILENAME'), filename)
		command = join(split(command, '&I'), suffix[i-1])
		for j in range(4):
			command = join(split(command, '&ARG'+str(j+1)), templates[template][i-1][j])
		if blocking:
			while (filename+'_'+suffix[i-1]+'_done' not in os.listdir(os.curdir)):
				pass #if block is true, wait until the file is there 
		shellcmd(command)

	# generate ending command...
	command = join(split(ending, '&FILENAME'), filename)
	command = join(split(command, '&TEMPLATE'), template)
	for j in range(4):
		command = join(split(command, '&ARG'+str(j+1)), templates[template][4][j])
	shellcmd(command)

	# copy the phone version to the print version so the printing computer will see it...
	if template == 'phone-2x3':
		print 'template', template
		shellcmd('cp '+filename+'_'+template+'.jpg '+filename+'_print-2x3.jpg')

	# do this extra step to make a double print strip, 
	#    assumes use of 'phone' template/ending file...
	#    (requires a vertical 2000x6000 final composite image to start)
	if generateprint and template=='phone-2x3': 
		print 'template:', template
		shellcmd('gm composite -geometry +0+0 ' + filename +'_'+ template + '.jpg images/background-big.jpg -quality 100 done.jpg')
		shellcmd('gm composite -geometry +2001+0 ' + filename +'_'+ template +'.jpg done.jpg -quality 100 done.jpg')
		template = template[5:]
		shellcmd('gm convert -stroke gray -draw "line 2000,0 2000,6000" done.jpg -quality 95 ' + filename + '_print'+template+'.jpg')
	if generateprint and template=='phone-1x3': 
		print 'template:', template
		shellcmd('gm composite -geometry +0+0 ' + filename +'_'+ template + '.jpg images/background-big2k3k.jpg -quality 100 done.jpg')
		shellcmd('gm composite -geometry +1001+0 ' + filename +'_'+ template +'.jpg done.jpg -quality 100 done.jpg')
		template = template[5:]
		shellcmd('gm convert -stroke gray -draw "line 1000,0 1000,3000" done.jpg -quality 95 ' + filename + '_print'+template+'.jpg')

# generate print fascade to generate_composite...
def generate_print(template, filename, blocking=True, generateprint=True):
	generate_composite(template, filename, blocking, generateprint)

# delete the temporary files created during creation of composites...
def cleanup_temp_files(filename):
	# remove temp files...
	shellcmd('rm *output.jpg done.jpg '+filename+'*done')


# open the USB video camera for use...
def startvid():			
	global x, y, video
        video = v4l2capture.Video_device('/dev/video0')
        x, y = video.set_format(1280, 720, fourcc='MJPG')
	video.create_buffers(1)
        video.queue_all_buffers()
	video.start()

# function to grab the sequence of raw images. 
#    copies dummy images to a new 'filename' for testing 
#    so that camera does not need to be used...
def grab_image(filename, i, usecamera=True):
	# Only capture image if it's one of the four... 
	if i in range(4): 
		# grab from camera or make a copy of the dummy images (for testing...)
		buff = StringIO()	# create StringIO buffer for stashing image data
		for jj in range(3 ):
			select.select((video,), (), ())
			image_data = video.read_and_queue()	# grab image from camera
			buff.write(image_data)			# stash in buff
			buff.seek(0)				# reset file pointer to zero...
			im = Image.open(buff)			# read image from buff
			buff.seek(0)
		ix, iy = im.size
		im.crop( (100, 0, ix-100, iy) ).resize( (1620, 1080), Image.ANTIALIAS ).save(filename+'_'+suffix[i]+'.jpg')

	# create flag file indicating that photo file download from camera completed...
	#shellcmd('gm convert -shave 100x0 '+filename+'_'+suffix[i]+'.jpg '+filename+'_'+suffix[i]+'.jpg')
	open(filename+'_'+suffix[i]+'_done', 'w').write('done') 


# move files into local subdirectories, SAMBA share, or web root at 'path'
def move_files(filename, path='/media/PHOTOBOOTH/', copy=True):
      if copy: cmd='cp '
      else: cmd='mv '
      try:
	print
	print 'filename = ', filename
	print cmd+'raw images...'
	shellcmd(cmd+filename+'_[a-d].jpg '+path+'raw-images')
	print cmd+'phone image...'
        shellcmd(cmd+filename+'_phone*.jpg '+path+'for-phone')
	print cmd+'print images...'
        shellcmd(cmd+filename+'_print*.jpg '+path+'for-print')
	print cmd+'display image...'
        shellcmd(cmd+filename+'_display*.jpg '+path+'for-display')
	print cmd+'lastone.txt...'
	shellcmd(cmd+'lastone.txt '+path)
      except:
	print 'PROBLEMS!!'


# Set sizes for screen, camera image and display...
#  -> here we can account for dissimilar aspect ratios of the images...
#size = width, height = 960, 540
#camerasize = camw, camh =  810,540
size = width, height = 1920, 1080
#size = width, height = 1280, 1024
scrsize = scrw, scrh =  1920, 1080
scrloc = (width-scrw)/2, (height-scrh)/2
#camerasize = camw, camh =  1280, 720
#camerasize = camw, camh =  1080, 720
camerasize = camw, camh =  1620, 1080
cameraloc = (width-camw)/2, (height-camh)/2
#dispsize = disw, dish = 1056, 720
dispsize = disw, dish = 1584, 1080
disploc = (width-disw)/2, (height-dish)/2


# define colors for easy of use with pygame...
black = (0,0,0)
white = (255,255,255)

# turn off all lights on button box...
def lightsoff():
	ser.write(str(0)) #turn off all lights...

# blink the output connected to the EL wire wrapped around the DSLR lens...
def blinklenslight():
	for i in range(5):
		ser.write(str(8)) # flash lens ring lighjt
		time.sleep(0.04)
		ser.write(str(0))
		time.sleep(0.04)
	ser.write(str(8))	# leave lens ring light on when done...

# wait for specific key(s) in a list, with a timeout (default is essentially forever)
def waitforkey(key, quitable = True, timeout = 99999999):
	# check for button lighting...
	if len(key)==1: # looking for a specific key, so light just that one...
		ser.write(str(0))
		time.sleep(0.1)
		if key[0]==K_g: ser.write(str(4))
		if key[0]==K_y: ser.write(str(2))
		if key[0]==K_r: ser.write(str(1))
		blink = False
	else: 
		blink = True
		blinky = 0

	userkey = False
	while not(userkey):
	   if timeout > 0:
		timeout -= 1
		time.sleep(0.2)
		if blink:
			ser.write(str(buttonpattern[blinky]))
			if blinky<len(buttonpattern)-1: blinky += 1
			else: blinky = 0
		for event in pygame.event.get():
			#print repr(event)
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN: 
				#print 'keydown...'
				if event.key in key:
					ser.write(str(0)) # turn off button lights... 
					return event.key
				if quitable and event.key == K_q: sys.exit()
	   else:
		# if we end up here, we timed out. Return "t" key...
		return K_t
	pygame.event.clear()

# fill the screen with a solid color...
def fillscreen(screen, color):
	screen.fill(color)
	pygame.display.flip()

# display an image on the screen, given the filename, specified size, and a location (allows centering)
def displayimage(screen, filename, csize, location=(0,0)):
		image = pygame.image.load(filename)
		imagerect = image.get_rect()
		image = pygame.transform.scale(image, csize)
		screen.blit(image, location)
		pygame.display.flip()

# an old function to flash text on the screen before taking the photo...
def flashtext(duration, rate, screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgblack = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgblack = bgblack.convert()
	bgwhite.fill(white)
	bgblack.fill(black)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, 128)
	textw = font.render(text, 1, white)
	textb = font.render(text, 1, black)
	textwpos = textw.get_rect()
	textbpos = textb.get_rect()
	if location==None:
		textwpos.centerx = textbpos.centerx = bgwhite.get_rect().centerx	
		textwpos.centery = textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textwpos.centerx = textbpos.centerx = w
		textwpos.centery = textbpos.centery = h
	bgwhite.blit(textb, textbpos)
	bgblack.blit(textw, textbpos)

	start = time.time()
	while (time.time()-start < duration):
		screen.blit(bgblack, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)
		screen.blit(bgwhite, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)


# function to write text on the screen with size and at location...
def showtext(screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgwhite.fill(black)#white)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, size)
	textb = font.render(text, 1, white)#black)

	textbpos = textb.get_rect()
	if location==None:
		textbpos.centerx = bgwhite.get_rect().centerx	
		textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textbpos.centerx = w	
		textbpos.centery = h
	bgwhite.blit(textb, textbpos)

	screen.blit(bgwhite, (0,0))
	pygame.display.flip()




