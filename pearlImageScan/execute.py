# -*- coding: utf-8 -*-
"""
Created on Sun May 15 21:31:19 2022

@author: pete
"""

# code to scan a series of images and send via text message 

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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

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



# send message with attachment 
# ========================================================