# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 14:18:48 2022

@author: Pete
"""

# testing the ability to open a web browser using python 

# using built in python package
# ============================================================
import webbrowser # no install needed, part of the standard library

webbrowser.open('http://www.espn.com', new = 1, autoraise = True) 

# using system prompt 
# ============================================================
from os import system
# chrome path
# chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
# must have an accurate chrome application path for this to run 
chromePath = "\"C:\Program Files\Google\Chrome\Application\chrome.exe\""
urlText = 'www.espn.com'
# system("\"C:\Program Files\Google\Chrome\Application\chrome.exe\" -incognito -new-window "  + urlText)
system(chromePath +  " -incognito -new-window "  + urlText)

# to resize a google chrome window, may need to connect to the api 
# may want to zoom out to 70% as well 
# > this is an example of one that would be a pro




# a package called "pupateer" [called pypateer for python]
# this one works pretty well! gonna use it for now
# ============================================================

import pyppeteer # pip install pyppeteer


browser = await launch()
page = await browser.newPage()
await page.goto('https://espn.com')

content = await page.evaluate('document.body.textContent', force_expr=True)

screenshotPath = "C:\\Users\\Pete\\Downloads\\"

# update the working directory to downloads 
import os 
os.chdir(screenshotPath)
os.getcwd()

# the below works!! but does not actually open the browser [which is prob what we want ]
browser = await launch()
page = await browser.newPage()
await page.goto('http://espn.com')
await page.screenshot({'path': 'example.png'})
await browser.close()

# try making the window bigger for the screenshot 
# this one works too! 
browser = await launch()
page = await browser.newPage()
await page.setViewport({"width": 1600, "height": 900})
await page.goto('http://espn.com')
await page.screenshot({'path': 'example2.png'})
await browser.close()

# try one more time with a zoom out 
# couldn't figure out a zoom out, but have the ability to screenshot the entire "scrollable page" 
browser = await launch()
page = await browser.newPage()
await page.setViewport({"width": 1600, "height": 900})
await page.goto('http://espn.com')
await page.screenshot({'path': 'example3.png', 'fullPage':True})
await browser.close()

# if the zoom out works, then test it's runability via task scheduler 





# google chrome api [still need to research this one]
# ============================================================
# using the peter.standbridge@gmail.com account