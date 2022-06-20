# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:52:20 2022

@author: Pete
"""

# script to dynamically crop an image based on some sort of key

# install packages & define directory 
import os 
import pyppeteer # pip install pyppeteer
import pandas as pd
wd = "C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\"
fileName1 = "screenshot1.png"
fileName2 = "screenshot2.png"
fileName3 = "screenshot3.png"
os.chdir(wd)
os.getcwd()

# define the url paths
urlPath1 = "https://twitter.com/ohthatsNajee22/status/1538579065782689792?s=20&t=66gWHqxwrBSRrkQd74DB_Q"
urlPath2 = "https://twitter.com/_TJWatt/status/1538549305694363648?s=20&t=66gWHqxwrBSRrkQd74DB_Q"
urlPath3 = "https://twitter.com/steelers/status/1538886386136276992?s=20&t=66gWHqxwrBSRrkQd74DB_Q"

# grabbing the screenshots 
import asyncio
import nest_asyncio
nest_asyncio.apply()

import time

# image 1 
async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    await page.goto(urlPath1)
    time.sleep(5)
    await page.screenshot({'path': fileName1, 'fullPage':True})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

# image 2 
async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    await page.goto(urlPath2)
    time.sleep(5)
    await page.screenshot({'path': fileName2, 'fullPage':True})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

# image 3
async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    await page.goto(urlPath3)
    time.sleep(5)
    await page.screenshot({'path': fileName3, 'fullPage':True})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

# crop them down a little bit manually for easier readability 
# [could remove this when i add the dynamic cropping]
from PIL import Image # pip install Pillow
myImage1 = Image.open(wd + '\\' + fileName1)
width, height = myImage1.size 
left = 0 
top = 0 
right = width
bottom = 1015
myNewImage = myImage1.crop((left, top, right, bottom))
myNewImage.save(wd +'\\temp1.png',optimize=True,quality=95)
newFile1 = 'temp1.png'

myImage2 = Image.open(wd + '\\' + fileName2)
width, height = myImage2.size 
left = 0 
top = 0 
right = width
bottom = 1015
myNewImage = myImage2.crop((left, top, right, bottom))
myNewImage.save(wd +'\\temp2.png',optimize=True,quality=95)
newFile2 = 'temp2.png'

myImage3 = Image.open(wd + '\\' + fileName3)
width, height = myImage3.size 
left = 0 
top = 0 
right = width
bottom = 1100
myNewImage = myImage3.crop((left, top, right, bottom))
myNewImage.save(wd +'\\temp3.png',optimize=True,quality=95)
newFile3 = 'temp3.png'

# ============================================================
# here is where i actually mess around with the
# DYNAMIC CROPPING!!! 
# ============================================================