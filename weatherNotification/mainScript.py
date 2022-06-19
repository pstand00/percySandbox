# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 13:18:38 2022

@author: Pete
"""

# query set to: 
# - grab a screenshot for the weather channl's dc hourly weather
# - send it to my phone via text message


# install packages & define directory 
import os 
import pyppeteer # pip install pyppeteer
import pandas as pd
from email.mime.base import MIMEBase
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
wd = "C:\\Users\\Pete\\Documents\\Projects\\Weather Notification\\screenshotFiles"
fileName = "screenshot.png"
os.chdir(wd)
os.getcwd()

# navigate to the webpage and save as screenshot 
urlPath = "https://weather.com/weather/hourbyhour/l/5589521886a4a0f93b5dc80125518029899488a1fc0f80e4662080ff41b1ed1d"
# browser = await launch()
# page = await browser.newPage()
# await page.setViewport({"width": 1600, "height": 900})
# await page.goto(urlPath)
# await page.screenshot({'path': fileName, 'fullPage':True})
# await browser.close()


# test using the function 
import asyncio

import nest_asyncio
nest_asyncio.apply()

async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    await page.goto(urlPath)
    await page.screenshot({'path': fileName, 'fullPage':True})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())



# crop to an arbitrary % for readability 
from PIL import Image # pip install Pillow
myImage = Image.open(wd + '\\' + fileName)
width, height = myImage.size 
left = 0 
top = 0 
right = width
bottom = 1015
myNewImage = myImage.crop((left, top, right, bottom))
myNewImage.save(wd +'\\temp.png',optimize=True,quality=95)
newFile = 'temp.png'

# making much smaller [not a real solution ]
# from PIL import Image # pip install Pillow
# My image is a 200x374 jpeg that is 102kb large
# foo = Image.open(wd + '\\' + fileName)
# downsize1 = foo.size[0] * 0.2
# downsize2 = foo.size[1] * 0.2
# foo2 = foo.resize((int(downsize1),int(downsize2)))
# I downsize the image with an ANTIALIAS filter (gives the highest quality)
# The saved downsized image size is 24.8kb
# foo2.save(wd +'\\temp.png',optimize=True,quality=95)
# The saved downsized image size is 22.9kb
# newFile = 'temp.png'

# send the email
fromEmail = "peter.standbridge@gmail.com"
toEmail = "4126805149@mms.att.net"
pwdPath = 'C:\\Users\\Pete\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()

msg = MIMEMultipart("alternative")
# msg["Subject"] = "SubjectLine"
msg["From"] = fromEmail
msg["To"] = toEmail
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
 
# delete the file 

os.remove(wd +'\\' + fileName)
os.remove(wd +'\\' + newFile)