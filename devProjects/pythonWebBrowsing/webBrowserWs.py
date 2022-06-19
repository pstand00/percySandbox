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


# google chrome api 
# ============================================================
# using the peter.standbridge@gmail.com account