import smtplib
import ftplib
import os
from credentials import *

def socialpost(filename, FBpost=False):
    # upload the file to an xternal web server...
    print 'Uplading', filename, 'to', ftphost
    session = ftplib.FTP(ftphost, ftpname, ftppass)
    imagefile = open(filename, 'rb')
    if 'display' not in filename and ( '_a.jpg' in filename or '_b.jpg' in filename or '_c.jpg' in filename or '_d.jpg'):
        # change directory if these are the raw images...
        session.cwd('raw-images')
        session.storbinary('STOR '+filename, imagefile)
    else:
        session.storbinary('STOR '+filename, imagefile)
    imagefile.close()
    session.quit()

    if FBpost:
       print 'Posting', filename, 'to Facebook...'
       # send email trigger to IFTTT with link to image we just uploaded...
       server = smtplib.SMTP_SSL(smtphost, 465) # use SSL...
       server.ehlo()
       server.login(smtpname, smtppass)
       FROM = smtpname
#       TO = ['trigger@recipe.ifttt.com'] #must be a list
       TO = ['laurenpercy@freescale.com'] #must be a list
       SUBJECT = "#FTF2015selfie" # hashtag trigger for IFTTT...
       TEXT = webhost + filename

       message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ",".join(TO), SUBJECT, TEXT)
       server.sendmail(FROM, TO, message)
