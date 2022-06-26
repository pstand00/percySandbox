# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 12:03:34 2022

@author: Pete
"""


# using selenium
# ============================================================
# need to download a seperate driver here: https://www.geeksforgeeks.org/click-button-by-text-using-python-and-selenium/
# its called "chrome driver" instead of just "chrome" 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# other required packages 
import time
import pandas as pd

# read in the ig credentials 
pwdPath = 'C:\\Users\\Pete\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
igUserName = pwdDf[['instagram_steelersTweets']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
igPassword = pwdDf[['instagram_steelersTweets']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()


# driver = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,720")
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe")
# driver.close()
driver.get("http://www.instagram.com")#put here the adress of your page
time.sleep(5)

# the below works!!!
# button = driver.find_element_by_link_text("Sign up")
# button = driver.find_element_by_link_text("Password")
# button = driver.find_element('Password')
button = driver.find_element_by_css_selector('input')
button.click()
# add text to current selection 
actions = ActionChains(driver) 
actions.send_keys('steelerstweets')
actions.perform()
# send a tab
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB)
actions.perform()
# insert password 
actions = ActionChains(driver) 
actions.send_keys('Franks.redhot.1993')
actions.perform()
# send an enter
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(5)
# click the 'not now' button 
# button = driver.find_element_by_css_selector('button')
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * 2)
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(5)
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * 2)
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()

# select the "new post" window 
# was able to find this in developer tools 

# find the new post button by name 
time.sleep(2)
newPostButtonAll = driver.find_elements_by_class_name('_ab6-')
newPostButton = ''
for i in newPostButtonAll:
    # print(i.text)
    print(i.get_property('attributes')[0]['nodeValue'])
    nodeVal = i.get_property('attributes')[0]['nodeValue']
    if 'New post' in nodeVal:
        print('this is our button')
        newPostButton = i 
    else:
        print('keep lookin')
    
newPostButton.click()


# find the "select from computer" button by name 

# click "select from cmputer"
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB)
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
#app = Application()

time.sleep(5)

# same deal for pywinauto
# this one might do it .... 
from pywinauto import Desktop

lastWindow = ''
currWindow = ''
lastObj = ''
currObj = ''
aa = ''
filePath = "C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png"
# list every open windo w
windows = Desktop().windows()
time.sleep(2)
for i in windows:
    if i.window_text() == '':
        print('skip it')
        # do nothing 
    else:
        print(i.window_text())
        lastWindow = currWindow
        lastObj = currObj
        currWindow = i.window_text()
        currObj = i
        print(lastWindow + '.zzzz')
        if 'Instagram' in currWindow and lastWindow == 'Open':
            print('this is the window we want to manipulate!!')
            aa = lastObj
            bb = lastWindow
            # lastObj.click(button = 'left')
            # lastObj.close()
            # sys.exit()
            # lastObj.click(button = 'left')
            # lastObj.type_keys('my path here!!!')
            lastObj.type_keys(filePath, with_spaces=True)
            time.sleep(2)
            lastObj.send_keystrokes('{ENTER}')
            print('ok, were done manipulating!!')
    
    
# resize the photo to "original"
time.sleep(1)
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * 3)
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(1)
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * 6)
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()

# find next key [or just do 9 tabs]
nextButton = driver.find_elements_by_class_name("_acan._acao._acas")
# nextButton = driver.find_elements_by_css_selector("button")
nextButton2 = ''
for i in nextButton:
    print(i.text)
    print(i.get_property('attributes')[1]['nodeValue'])
    nodeVal = i.get_property('attributes')[1]['nodeValue']
    if i.text == 'Next':
        nextButton2 = i
     
        
nextButton2.click()

# find the next key again 
time.sleep(2)
filterNextButton = driver.find_elements_by_class_name("_acan._acao._acas")
# filterNextButton = driver.find_elements_by_css_selector("button")
filterNextButton2 = ''
for i in filterNextButton:
    print(i.text)
    print(i.get_property('attributes')[1]['nodeValue'])
    nodeVal = i.get_property('attributes')[1]['nodeValue']
    if i.text == 'Next':
        filterNextButton2 = i

filterNextButton2.click()

# 4 tabs to get to the caption window 
time.sleep(2)
captionWindow = driver.find_elements_by_css_selector('textarea')
captionWindow2 = ''
for i in captionWindow:
    # print(i.get_property('attributes')[0])
    nodeVal = i.get_property('attributes')[0]['nodeValue']
    if 'caption' in nodeVal:
        print('this is our text box')
        captionWindow2 = i 
    else:
        print('keep lookin')
        
captionWindow2.click()
# insert caption 
actions = ActionChains(driver) 
actions.send_keys('www.com')
actions.perform()

# find the share button 
shareButton = driver.find_elements_by_class_name("_acan._acao._acas")
shareButton2 = ''
for i in shareButton:
    print(i.text)
    if i.text == 'Share':
        shareButton2 = i

shareButton2.click()

time.sleep(4)

driver.close()


# works live, but not working on headless 
