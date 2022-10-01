#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 13:21:32 2022

@author: pete
"""

# ================================================================
# test file to make sure i can run stuff from the command prompt 
# ================================================================


# load libraries 
import os
import subprocess
import sys 
import datetime
import re 
# need to figure out why this isn't working in spyder
import pandas as pd 
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import email
from email.mime.base import MIMEBase


# refer to pw file 
# define working directory and date and passwords
# ========================================================
userPath = '/Users/pete'
# currentTimestampUtc = datetime.datetime.utcnow()
# currentTimestampEst = currentTimestampUtc.astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
currentTimestampEstDt = datetime.datetime.now()
# currentTimestampEstDt = datetime.datetime.strptime(currentTimestampEst,"%Y-%m-%d %H:%M:%S")
currentDayOfWeek = currentTimestampEstDt.strftime('%A')
fromEmail = "peter.standbridge@gmail.com"
toEmail = "4126805149@mms.att.net"
pwdPath = userPath + '/Documents/System Scripts/secrets.json'
pwdDf = pd.read_json(pwdPath)
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()


# find the image to emial 
imagePath = userPath + '/Downloads/200.gif'
imagePath = userPath + '/Downloads/IMG_8055.jpg'

# send email message 
emailTxt = 'Happy ' + currentDayOfWeek + ' from Pete\'s Mac'
msg = MIMEMultipart("alternative")
# msg["Subject"] = "SubjectLine"
msg["From"] = fromEmail
msg["To"] = toEmail
bodyMime = MIMEText(emailTxt)
msg.attach(bodyMime)
# Open PDF file in binary mode
with open(imagePath, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {imagePath}",
)

# Add attachment to message and convert message to string
msg.attach(part)

# send the actual note
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(emailUser, emailPw)
server.sendmail(fromEmail, toEmail, msg.as_string())


