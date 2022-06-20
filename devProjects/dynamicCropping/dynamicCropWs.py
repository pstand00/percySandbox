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
import io 
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

import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image
import cv2 #  pip install opencv-python
import csv

# must specify the path of the external program needed to pars out the data 
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# image 1 - the first attempt to get it working, but a lil sloppy
# ============================================================
dynImage1 = Image.open(newFile1)
imageData1 = pytesseract.image_to_boxes(dynImage1)
results = pytesseract.image_to_data(dynImage1)
resultsDf = pd.read_csv(io.StringIO(results), sep = '\t')

resultsDfLite = resultsDf[(resultsDf['text'] == 'Retweets') ]
retweetsTop = int(resultsDfLite['top'].to_string(index=False, header= False).strip())

# writeImageData to csv

# convert imageData1 index to a string 
imageDf1 = pd.read_fwf(io.StringIO(imageData1), header = None)
fullText1 = ''
for i in imageDf1[0]:
    #newTxt = i.to_string(index=False, header= False).strip()
    print(fullText1)
    print(i)
    fullText1 = fullText1 + i 
    print(fullText1)
    
    
# find the location of the word "Retweet" [Nth character]
rtLoc1 = fullText1.find('Retweet')
# then, pull then Nth row from imageData1 to get the pixel position 
rtLocDf1 = imageDf1.iloc[rtLoc1]
rtPosFinal = rtLocDf1[1]
# then, crop at that location + 10 or so 
width, height = dynImage1.size 
left = 0 
top = 0 
right = width
bottom = retweetsTop # rtPosFinal # nned to get this dynamically from image_to_data() function
myNewImage = dynImage1.crop((left, top, right, bottom))
myNewImage.save(wd +'\\final1.png',optimize=True,quality=95)
newFile = 'final1.png'


# image 2 - only the required commands (although still need packages from above )
# ============================================================
dynImage2 = Image.open(fileName2)
textLocResults2 = pytesseract.image_to_data(dynImage2)
textLocResultsDf2 = pd.read_csv(io.StringIO(textLocResults2), sep = '\t')
# find the location of the word "Retweet" [Nth character]
textLocResultsDfLite2 = textLocResultsDf2[(textLocResultsDf2['text'] == 'Retweets') ].head(1)
retweetsTop2 = int(textLocResultsDfLite2['top'].to_string(index=False, header= False).strip())
# then, crop at that location + 10 or so 
width, height = dynImage2.size 
left = 0 
top = 0 
right = width
bottom = retweetsTop2 # rtPosFinal # nned to get this dynamically from image_to_data() function
bottom = retweetsTop2 - 25 # 25 was a good number to account for the twitter spacing 
myNewImage = dynImage2.crop((left, top, right, bottom))
myNewImage.save(wd +'\\final2.png',optimize=True,quality=95)
newFile = 'final2.png'

# image 3 - try to get the left and right figured out here 
# ============================================================
