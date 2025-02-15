# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:04:19 2025

@author: Pete
@purpose: script is meant to grab tasks from notion for pete's personal
    list, organize them in a specific way and send an email with the tasks 
    to be completed 
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
fm = 'C:\\Users\\Pete'
pwdPath = fm + '\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()
emailRecipient = emailUser

try:
    import requests
    import pandas as pd
    import numpy as np 
    pd.set_option('display.max_colwidth', -1)
    # email
    from email.mime.base import MIMEBase 
    from email import encoders 
    # sample error below 
    # aa = bb

except Exception as e:
    # print(e)
    errorText = str(e)
    # emailText = '<html><font color = "#404041"><font face = "monospace">Something went wrong with the Phrase Mapping Load process. Please review and try again. The script lives here "C:\\Users\\peter.standbridge\\Documents\\reportingAndAnalyticsTeam\\peteSandbox\\adHoc\\202501_addressLatLong"</font>' + str(e)
    # string the email text together 
    emailText = '<html><font color = "#404041"><font face = "monospace">' 
    emailText = emailText + '<p>Something went wrong with the Personal Task Notification process. Please see the error message below:<p/>'
    emailText = emailText + '<p><bold><font color = "#e65c00">' + errorText + '</font></bold></p>'
    emailText = emailText + '<p>Please review the script here: "C:\\Users\\Pete\\Documents\\GitHub\\percySandbox\\personalTaskNotifications"<p/>'
    emailText = emailText + '</font></font>'
    # end of the string 
    subjectTxt = '=?utf-8?Q?=F0=9F=8E=BA?='  + " Something's wrong with the Personal Task Notification process"
    #F0 9F 8E BA
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subjectTxt
    msg["From"] = "Automated Notification <" + emailUser + ">"
    msg["To"] = "Automated Recipients <" + emailRecipient + ">"
    bodyMime = MIMEText(emailText, "html")
    msg.attach(bodyMime)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(emailUser, emailPw)
    server.sendmail(emailUser, emailRecipient, msg.as_string())

