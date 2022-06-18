# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 13:54:36 2022

@author: Pete
"""

# screenshot test 

# currently going off of the following article
# https://datatofish.com/screenshot-python/

import pyautogui # pip install pyautogui

screenshotPath = "C:\\Users\\Pete\\Downloads\\screenshot.png"

myScreenshot = pyautogui.screenshot()
myScreenshot.save(screenshotPath)

# this works!! 