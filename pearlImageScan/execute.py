# -*- coding: utf-8 -*-
"""
Created on Sun May 15 21:31:19 2022

@author: pete
"""

# code to scan a series of images and send via text message 

## add a try statement that only texts me if there's an error 
## see if i can "force" what the "email text is from" [ie "my austomation" instead of "peterstandbridge@gamil"]

# req packages 
# ========================================================
import os
import subprocess
import sys
import datetime
import pytz # allows for time zone conversion 
import re
import pandas as pd
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import email
from email.mime.base import MIMEBase


# define working directory and date and passwords
# ========================================================
wFm = os.getenv('userprofile')
currentTimestampUtc = datetime.datetime.utcnow()
currentTimestampEst = currentTimestampUtc.astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
currentTimestampEstDt = datetime.datetime.strptime(currentTimestampEst,"%Y-%m-%d %H:%M:%S")
currentDayOfWeek = currentTimestampEstDt.strftime('%A')
fromEmail = "peter.standbridge@gmail.com"
toEmail = "4126805149@mms.att.net"
pwdPath = wFm + '\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()


# scan file names and select one at random 
# ========================================================
imageDir = wFm + '\\Documents\\images\\pearlPics'
imageList = os.listdir(imageDir)
imageDf = pd.DataFrame({'fileName':[], 'randoNum':[]})
for i in imageList:
    print(i)
    rando = random.random()
    imageDf = imageDf.append(pd.DataFrame({'fileName':[i], 'randoNum':[rando]}))

# pick the max random number 
imageDfOrder = imageDf.sort_values(by = 'randoNum').head(1)
fileName = imageDfOrder['fileName'].to_string(index=False, header= False).strip()
filePath = imageDir +'\\' + fileName
os.chdir(imageDir)


# resize the image so that it can be sent as an email 
# ========================================================
from PIL import Image # pip install Pillow
# My image is a 200x374 jpeg that is 102kb large
foo = Image.open(filePath)
downsize1 = foo.size[0] * 0.25
downsize2 = foo.size[1] * 0.25
foo2 = foo.resize((int(downsize1),int(downsize2)))
 # I downsize the image with an ANTIALIAS filter (gives the highest quality)
 # The saved downsized image size is 24.8kb
foo2.save(imageDir +'\\temp.png',optimize=True,quality=95)
# The saved downsized image size is 22.9kb
newFile = 'temp.png'


# send message with attachment 
# ========================================================
# emailTxt = 'This is a test message 2 '
emailTxt = 'Happy ' + currentDayOfWeek + ' from Ms. Pearl'
msg = MIMEMultipart("alternative")
# msg["Subject"] = "SubjectLine"
msg["From"] = fromEmail
msg["To"] = toEmail
bodyMime = MIMEText(emailTxt)
msg.attach(bodyMime)
# Open PDF file in binary mode
with open(newFile, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {newFile}",
)

# Add attachment to message and convert message to string
msg.attach(part)

# send the actual note
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(emailUser, emailPw)
server.sendmail(fromEmail, toEmail, msg.as_string())

# delete the temp pic 
os.remove(imageDir +'\\temp.png')