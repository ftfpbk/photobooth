#!/usr/bin/python
# many dependencies are all brought in with this import...
from libphotobooth import *
from libsocialmedia import *

#=============================================================================
# ========================= COMMAND LINE ARGUMENTS ===========================
#=============================================================================
if 'help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
	print """
NAME: 
	photobooth.py  -  a photo booth python script

OPTIONS:
	-h,--help,help	print help
	nousecamera	use dummy photos instead of camera (default: USB connected camera)
	nomove		do not move images after processing (default: move)
	lastphoto=xxxx	begin sequence with the provided 4-digit (>=1000) number 
	noincrement	do not increment the image sequence number (default: increment)
	doubleprint	generate the double print (adds time, default: no doubleprint)
	sepia		do composites in sepia tone
	bw		do composites in black and white
	1x3		generate phone at 1000x3000 reslution (faster) for double prints
	2x6		generate phone and print in 2000x3000 resolution (faster)
	4x6		generate phone and print in 4000x6000 resolution (too slow)
	regen=DSCxxx	filename to regenerate
	location=<path>	path to raw images with _a, _b, _c, _d suffixes of filename
	nodisplay	do not use the graphical display or delays with them (default = true)
	recurse		used with regen to generate composites from all photos in raw directory

DESCRIPTION:
	This python script implements a photo booth where a sequence of four images is 
	taken by a USB-connected camera and processed into various composite images.

	Requires: libgphoto2, python-pygame, piggyphoto (python binding for libgphoto2)
	and graphicsmagick.

"""
	sys.exit()

# use camera or dummy source images...
if 'nousecamera' in sys.argv:
	camera_arg=False
else:
	camera_arg=True

if 'doubleprint' in sys.argv:
	doubleprint=True
else:
	doubleprint=False

if 'nodisplay' in sys.argv:
	display = False
else:
	display = True

# use sepia tone...
default_tone = '1x3'
if 'sepia' in sys.argv and not('bw' in sys.argv):
	default_tone = '-sepia'
if 'bw' in sys.argv and not('sepia' in sys.argv):
	default_tone='-bw'
if '4x6' in sys.argv and not('sepia' in sys.argv) and not('bw' in sys.argv):
	default_tone='-4x6'
if '2x3' in sys.argv and not('sepia' in sys.argv) and not('bw' in sys.argv):
	default_tone='-2x3'
if '1x3' in sys.argv and not('sepia' in sys.argv) and not('bw' in sys.argv):
	default_tone='-1x3'

# move the files when done? Assume true...
move=True
if 'nomove' in sys.argv:
	print 'Not moving files...'
	move=False

# set lastphoto via command line... 
lastphoto=False
for i in sys.argv:
	if 'lastphoto' in i:
		lastphoto = True
		temp = split(i, '=')[1]
		break
if not(lastphoto):
	# this should be rolled into the filename function but for now it's here...
	last = eval(open('lastphoto', 'r').read())
	print 'Change current photo number '+str(last)+'?'
	#temp = raw_input( 'Enter valid new number or nothing to keep: ')
	temp = str(last)
	print "Using lastphoto..." , temp
if temp not in ['']: 
	last = eval(temp)
	open('lastphoto', 'w').write(str(last))
	open('/home/debian/photobooth/lastphoto','w').write(str(last))

# increment output photo index? default is true...
increment=True
if 'noincrement' in sys.argv:
	increment = False

# for regenerating a photo, need to specify base filename and location of raws...
regenerate = False
for i in sys.argv:
	if 'regen' in i:
		regenerate = True
	if 'location' in i:
		location = split(i, '=')[1]

# regenerate all composite files from raws...
recurse = False
loop = xrange(10000) # effectively while(1)...
if 'recurse' in sys.argv and regenerate:
	recurse = True
	rawfiles = os.listdir(location+'raw-images/')
	loop = []
	for i in rawfiles:
		if i[0:7] not in loop: loop.append(i[0:7])
	loop.sort()

#=============================================================================
# ===================== DONE COMMAND LINE ARGUMENTS ==========================
#=============================================================================



#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# print command line args to console to verify...
print 'nousecamera:', repr(camera_arg)
print 'nomove:', repr(not(move))
print 'lastphoto:', last
print 'increment:', repr(increment)
print 'doubleprint:', repr(doubleprint)
print 'tone:', repr(default_tone)

# initialize pygame if we're using a display (the default...)
if display:
	pygame.init()
	screen = pygame.display.set_mode(size)
	pygame.mouse.set_visible(False)

# start the USB video camera...
startvid()

key = ''
keylist = [K_g, K_r, K_s, K_b, K_c ]
adminkey = [K_r, K_s, K_b, K_c]
while(key not in keylist):
	preview_image(screen, 1, progressbar=False, text='Aim camera')
	key = waitforkey(keylist,  timeout=1)
	print key

# this is the main loop...
#   loop was set up above and unless regenerating composite(s), it's essentially infinite...
tone = default_tone # holdover from the attempt at toning the images... not sure if can be deleted yet
for element in loop:
	# flush the key queue in the event that someone hit a key...
	# important when looping, not so much the first time into the loop...
	if display: pygame.event.clear()

	if display:
		fillscreen(screen, black)
		if default_tone in ['-1x3', '-2x3', '-4x6']:
			displayimage(screen, 'images/pushtostart-nochoice.jpg', scrsize, scrloc)
		else:	
			displayimage(screen, 'images/pushtostart.jpg', scrsize, scrloc)

		key = waitforkey(keylist)	
		if key in adminkey:
			print 'Admin key!!  - Do something here...'
			if key == K_r: # RED admin button
				# What happens here:
				# display shutdown notice on screen, issue command to remote display to 
				# shutdown, sleep to wait for it to  be received, delete the command for
				# the remote display so it does not shutdown on rebooting, and then signal
				# our own shutdown...
				showtext(screen, 'Shutting down...', 100)
				open('/var/www/html/command.txt','w').write('shutdown')
				time.sleep(20)
				shellcmd('touch /home/debian/shutdown')
				open('/var/www/html/command.txt','w').write('')
				time.sleep(120)
			if key == K_c: # YELLOW admin button
                                # What happens here:
                                # display reboot notice on screen, issue command to remote display to 
                                # reboot, sleep to wait for it to  be received, delete the command for
                                # the remote display so it does not reboot on rebooting, and then signal
                                # our own reboot...
                                showtext(screen, 'Rebooting system...', 100)
                                open('/var/www/html/command.txt','w').write('reboot')
                                time.sleep(20)
                                shellcmd('touch /home/debian/reboot')
                                open('/var/www/html/command.txt','w').write('')
                                time.sleep(120)

			continue

	if display:
		fillscreen(screen, black)
		displayimage(screen, 'images/fourphotostaken.jpg', scrsize, scrloc)
		time.sleep(1.7)
		fillscreen(screen, black)
		displayimage(screen, 'images/pushbuttontocontinue.jpg', scrsize, scrloc)
		print 'Push button to continue...'
		key = waitforkey(keylist, timeout=25)
		if key == K_t: continue	
		fillscreen(screen, black)
		flashtext(3, .75, screen, "Go stand by the wall", 100)

	# keep track of the starting time for some statistics...
	start = time.time()
	
	# get a new filename and print it to the console...
	if not(recurse):
		filename= new_filename(increment=increment)
	else: 
		filename = element # this comes from the raw directory...
	# filename is pre-filled above from command line... 
	print '\r\nnew filename:', filename

	# prime threads for compositing images...
	#    this was important when processing the 12MPixel images 
	#    from a DSLR, not so much from the USB webcam.
	t_ = []
	t_.append( threading.Thread(target=generate_composite, args=('display'+tone, filename)) )
	if not(doubleprint): t_.append( threading.Thread(target=generate_composite, args=('phone'+tone, filename)) )
	else: t_.append( threading.Thread(target=generate_print, args=('phone'+tone, filename)) )
	# start the queued threads...
	for i in t_: i.start()

	# grab the sequence of images from the camera (or, if specified, dummy images)...
	for i in range(4):
		if display:
			#showtext(screen, 'Image: '+str(i+1), 100)
			displayimage(screen, 'images/image'+str(i+1)+'.jpg', scrsize, scrloc)
			time.sleep(1.5)
		print 
		print 'Grabbing image: ', i+1
		if display: fillscreen(screen, black)
		if not(regenerate): 
			# get image from camera...
			preview_image(screen, 20)
			grab_image(filename, i, camera_arg)
		else:
			# if regenerate, copy from location the appropriate raw image...
			# and create semaphore file to indicate completion...
			print 'Copying:', location + filename+'_'+suffix[i] + '.jpg'
			shellcmd('cp ' + location + 'raw-images/' + filename+'_'+suffix[i] + '.jpg' + ' .')
			open(filename+'_'+suffix[i]+'_done', 'w').write('done') 
		if display: displayimage(screen, filename+'_'+suffix[i]+'.jpg', camerasize, cameraloc)
		print 'time to display:', time.time()-start
		if display: time.sleep(3)

	# wait until all compositing threads are complete...
	living=True
	displayed=False
	while ( living ):# or t_print.isAlive() ): 
		living=False
		if not displayed: 
		    	if display:	fillscreen(screen, black)
			time.sleep(0.5)
			if display: showtext(screen, 'Processing...', 100)
			time.sleep(0.5)
		else: time.sleep(1)
		print '    ===> still processing...'	
		for i in t_: 
			if i.isAlive(): living=True
		if not(t_[0].isAlive()) and not(displayed):
			displayed=True
			print 'time to display:', time.time()-start
			if display: 
				displayimage(screen, filename+'_display'+tone+'.jpg', dispsize, disploc)
				disptime = time.time()

	# this delay was thrown in because USB webcam images don't take nearly as long to composite...
	if time.time() - disptime < 10:
		time.sleep(10 - (time.time() - disptime) ) 

	print '\r\nAll images done:', time.time()-start
	time.sleep(1)

	# clean up the temporary files generated during compositing...
	cleanup_temp_files(filename)
	open('lastone.txt', 'w').write(filename)

	# upload and post to facebook...
	uploadall = True
        # start the queued threads...
	if uploadall == True:
		# create threaded queuefor uploading...
	        u_ = []
		print 
		print 'Queuing uploads...'
		for i in suffix:
			#socialpost(filename+'_'+i+'.jpg', FBpost=False)
			u_.append( threading.Thread(target=socialpost, args=(filename+'_'+i+'.jpg', False)) )
		#socialpost(filename+'_phone'+tone+'.jpg', FBpost=False)
		u_.append( threading.Thread(target=socialpost, args=(filename+'_phone'+tone+'.jpg', False)) )
		#if doubleprint: socialpost(filename+'_print'+tone+'.jpg', FBpost=False)
		if doubleprint: u_.append( threading.Thread(target=socialpost, args=(filename+'_print'+tone+'.jpg', False)) )
		#socialpost(filename+'_display'+tone+'.jpg', FBpost=True)
		u_.append( threading.Thread(target=socialpost, args=(filename+'_display'+tone+'.jpg', True)) )
		# start all items in the queue...
        	for i in u_: i.start()
		# now wait for all of them to finish...
		print 'Now wait for uploads to finish...'
		living = True
		while (living):
			living = False
			for i in u_:
                        	if i.isAlive(): living=True
			time.sleep(0.25)
		print 'Uploading done...'
		print


	# move files (default) to (redundant) location(s)...
	if move and not(regenerate):
		move_files(filename, path='/var/www/html/', copy=False)

	if move and regenerate:
		move_files(filename, path=location, copy=False)

	# print elapsed time to console...
	print '\r\nDone: ', time.time()-start


	# only do loop once if we're regenerating a set of composites...
	if regenerate and not recurse: break



