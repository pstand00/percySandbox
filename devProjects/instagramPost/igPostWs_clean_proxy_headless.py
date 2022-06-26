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


# attempting to find the random proxy 
# ============================================================

# documentation for proxy_randomizer available here: https://pypi.org/project/proxy-randomizer/
from proxy_randomizer import RegisteredProviders # pip install proxy_randomizer
from proxy_randomizer.proxy import Anonymity
rp = RegisteredProviders()
rp.parse_providers()

# generate a list of "anonymous" proxies
anonymous_proxies = list(
    filter(lambda proxy: proxy.anonymity == Anonymity.ANONYMOUS, rp.proxies)
)

print(f"filtered proxies: {anonymous_proxies}")

# loop through all proxies 
for i in anonymous_proxies:
    myCurrProxie = i.get_proxy()
    print(type(myCurrProxie))
    if 'United States' in str(i):
        print(i)
        print(myCurrProxie)
        print('on to the next one...')

# create a dataframe of only the us proxies 
ipDf = pd.DataFrame({'fullString':[], 'ip':[]})
for i in anonymous_proxies:
    currentProxy = i.get_proxy()
    print(type(myCurrProxie))
    if 'United States' in str(i):
        print(i)
        print(currentProxy)
        ipDf = ipDf.append(pd.DataFrame({'fullString':[str(i)], 'ip':[i.get_proxy()]}))
        print('added 1 row to the df')


# create a randomization factor 
import random
randoPick = [random.randint(1, 10)][0]
print(randoPick)

# proxy to use 
ipDfActive = ipDf.iloc[randoPick-1]
print(ipDfActive[1])
ipActive = ipDfActive[1]

# defining the chrome_options 
from selenium.webdriver.common.proxy import Proxy, ProxyType
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = ipActive
# prox.socks_proxy = ipActive
# prox.ssl_proxy = ipActive

capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

# driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", desired_capabilities=capabilities)

# end of proxy workspace 
# ============================================================

# attempting to use more specific actions on the headless functionality 
# ============================================================
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,720")
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options, desired_capabilities=capabilities)
driver.get("http://www.instagram.com")#put here the adress of your page
time.sleep(5)

# trying to find the phone number 
# ----------------------------------------------------------------
usernameObjectResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Phone number')]")
usernameObject = ''
for i in usernameObjectResults:
    print(i.text)
    if i.text == 'Phone number, username, or email':
        print('we found a winner!')
        usernameObject = i
        
actions = ActionChains(driver) 
# actions.move_by_offset(usernameObject.location['x'] + 2, usernameObject.location['y'] + 2).click()
actions.move_to_element(usernameObject).click_and_hold()
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(igUserName)
actions.perform()

# trying to find the password
# ----------------------------------------------------------------
passwordObjectResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Password')]")
passwordObject = ''
for i in passwordObjectResults:
    print(i.text)
    if i.text == 'Password':
        print('we found a winner!')
        passwordObject = i
        
actions = ActionChains(driver) 
actions.move_to_element(passwordObject).click_and_hold()
actions.perform()
actions = ActionChains(driver) 
actions.send_keys(igPassword)
actions.perform()

# send enter to go to the next screen 
# ----------------------------------------------------------------
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(5)

# select ("not now" on the second sheet )
# ----------------------------------------------------------------
page2ButtonResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Not Now')]")
page2Button = ''
for i in page2ButtonResults:
    print(i.text)
    if i.text == 'Not Now':
        print('we found a winner!')
        page2Button = i
        
page2Button.click()


time.sleep(2)

# actions = ActionChains(driver) 
# actions.move_to_element(page2Button).click_and_hold()
# actions.perform()

# select the ("new post" button )
# ----------------------------------------------------------------
newPostButtonResults = driver.find_elements_by_css_selector("[aria-label='New post']")
for i in newPostButtonResults:
    print(i.text)
    newPostButton = i 


newPostButton.click()

# locate the "select file from computer button"
# ----------------------------------------------------------------
# loadFileButtonResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Select from computer')]")
# loadFileButton = ''
# for i in loadFileButtonResults:
    # print(i.text)
    # if i.text == 'Select from computer':
        # print('we found a winner!')
        # loadFileButton = i
        
# actions = ActionChains(driver) 
# actions.move_to_element(loadFileButton).click_and_hold()
# actions.perform()

# loadFileButton.click()
# should be able to delete the above ^^^ 
# ---------------

time.sleep(1)

# attempt to run the file load 
# ----------------------------------------------------------------
inputFormResults = driver.find_elements_by_css_selector('input')
for i in inputFormResults:
    print(i.text)
    inputForm = i


inputForm.send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png")

time.sleep(2)

# finding the "Select crop" label 
# ----------------------------------------------------------------
selectCropButtonResults = driver.find_elements_by_css_selector("[aria-label='Select crop']")


for i in selectCropButtonResults:
    print(i.text)
    selectCropButton = i 


selectCropButton.click()

time.sleep(1)

# finding the "Original" label 
# ----------------------------------------------------------------
originalLabelResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Original')]")
originalLabel = ''
for i in originalLabelResults:
    print(i.text)
    if i.text == 'Original':
        originalLabel = i 



originalLabel.click()

time.sleep(1)

# finding the "Next" button
# ----------------------------------------------------------------
nextButtonResults1 = driver.find_elements_by_xpath("//*[contains( text( ), 'Next')]")
nextButton1 = ''
for i in nextButtonResults1:
    print(i.text)
    nextButton1 = i

nextButton1.click()

time.sleep(1)

# finding the "Next" button again 
# ----------------------------------------------------------------
nextButtonResults2 = driver.find_elements_by_xpath("//*[contains( text( ), 'Next')]")
nextButton2 = ''
for i in nextButtonResults2:
    print(i.text)
    nextButton2 = i

nextButton2.click()

time.sleep(1)

# trying to find the caption portion of the screen 
# ----------------------------------------------------------------
captionResults = driver.find_elements_by_css_selector('textarea')
caption = ''
for i in captionResults:
    print(i.text)
    print(i.get_property('attributes')[0]['nodeValue'])
    # print(i.get_property('attributes'))
    if 'Write a caption' in i.get_property('attributes')[0]['nodeValue']:
        caption = i

caption.click()
actions = ActionChains(driver) 
actions.send_keys('My caption <3')
actions.perform()

time.sleep(1)
    
# click the "share" button 
# ----------------------------------------------------------------
shareButtonResults = driver.find_elements_by_xpath("//*[contains( text( ), 'Share')]")
shareButton = ''
for i in shareButtonResults:
    print(i.text)
    if i.text == 'Share':
       shareButton = i


shareButton.click()

time.sleep(5)


# driver.save_screenshot("C:\\Users\\Pete\\Downloads\\headlessScreenshot.png")
driver.close()



# end of headless workspace 
# ============================================================











# !!!! the below is just test stuff ... everything above works 


# driver = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,720")
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
# driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe")
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
actions.send_keys('igPassword')
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
