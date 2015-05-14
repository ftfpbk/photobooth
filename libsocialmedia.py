import smtplib
import ftplib
import os
from credentials import *

def postFacebook(filename):
    # upload the file to an xternal web server...
    session = ftplib.FTP(ftphost, ftpname, ftppass)
    imagefile = open(filename, 'rb')
    session.storbinary('STOR '+filename, imagefile)
    imagefile.close()
    session.quit()

    # send email trigger to IFTTT with link to image we just uploaded...
    server = smtplib.SMTP_SSL(smtphost, 465) # use SSL...
    server.ehlo()
    server.login(smtpname, smtppass)
    FROM = smtpname
    TO = ['trigger@recipe.ifttt.com'] #must be a list
    SUBJECT = "#FTF2015selfie" # hashtag trigger for IFTTT...
    TEXT = 'http://happycamperphotobooth.com/boothpics/'+filename

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ",".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
