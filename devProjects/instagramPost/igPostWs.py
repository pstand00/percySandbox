# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 16:37:28 2022

@author: Pete
"""

# code to attempt to post an image to instagram programatically 



# try #1 - instabot package .. was not seemingly able to log in
# ============================================================
# set a current directory for a config file to be saved on 
import os
os.chdir("C:\\Users\\Pete\\Documents\\GitHub\percySandbox\\devProjects\\instagramPost")
from instabot import Bot # pip install instabot
bot = Bot()

bot.login(username = "steelerstweets",password = "pw")

file = open("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png", "r")
bot.upload_photo("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png",
           caption = "My Test Caption")
bot.upload_photo(file,
           caption = "My Test Caption")


os.remove("C:\\Users\\Pete\\Documents\\GitHub\percySandbox\\devProject\\instagramPost\\config")



# try #2 - using api syntax
# ============================================================




# try #3 - using web scrape crawler like 
# ============================================================
import pyppeteer # pip install pyppeteer
import asyncio
import nest_asyncio
nest_asyncio.apply()
import time

# navigate to the initial screen 
url = 'https://www.instagram.com/'
# https://www.instagram.com/
async def main():
   #  browser = await pyppeteer.launch()
    browser = await pyppeteer.launch(headless=False, executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' )
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    await page.goto(url)
    # try clicking the button that say sign up 
    content = "Password"
    await page.evaluate(f"""() => {{
        document.getElementById('myinput').value = '{content}';
    }}""")
    # btn = await page.Jx('//input[contains(text(), "Password")]')
    # page.$x('//span[text()="Sign up"]')
    #await page.goto(inProcessUrl, {"waitUntil" : "networkidle0"})
    time.sleep(10)
    # await page.screenshot({'path': screenshotFileName, 'fullPage':True})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


# login 

# click the new post button
# click "load photos from my computer" 
# actually select the photo [this could be hard]
# make the photo "original" size 
# click next
# click next again to not add a filter 
# select the caption area & insert url as caption 
# select share 

# try # 4 ... using selenium
# ============================================================
# need to download a seperate driver here: https://www.geeksforgeeks.org/click-button-by-text-using-python-and-selenium/
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

driver = webdriver.Chrome("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
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
actions.send_keys('myPassword')
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
newPostButtonAll = driver.find_elements_by_class_name('_ab6-')
newPostButton = ''
for i in newPostButtonAll:
    # print(i.text)
    print(i.get_property('attributes')[0])
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
nextButton2 = ''
for i in nextButton:
    print(i.text)
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

driver.close()









# other attempts that didn't pan out 
# ============================================================

actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * )
actions.perform()


print([w.window_text() for w in windows])







# still trying to load the file 
pywinauto.findwindows.find_window()


# 
import win32gui

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        windowName = 'win32gui.GetWindowText( hwnd )'

win32gui.EnumWindows( winEnumHandler, None )


# this one seems a lil cleaner
import pyautogui

lastWindow = ''
currWindow = ''
lastObj = ''
currObj = ''
for x in pyautogui.getAllWindows():  
    print(x.title)
    lastWindow = currWindow
    lastObj = currObj
    currWindow = x.title
    currObj = x
    print(lastWindow + '.zzzz')
    if 'Instagram' in currWindow and lastWindow == 'Open':
        print('this is the window we want to manipulate!!')
        sys.exit()
        lastObj.resizeTo(200, 200) 
        # select the current window 
        lastObj.activate()
        pyautogui.getWindowsWithTitle(lastWindow)[0].restore()
        pyautogui.write("Hello, world!")
        print('ok, were done manipulating!!')


# from here, should just be able to click the resize button
# click next 
# click next again to delete the filterss
# past the url in the caption 
# press share 
# close the window and go back to the rest of the script 




import win32con
hwnd = win32gui.GetForegroundWindow()


omniboxHwnd = win32gui.FindWindowEx(hwnd, 0, 'Chrome_OmniboxView', None)



from pywinauto import Desktop

chrome_window = Desktop(backend="uia").window(class_name_re='Chrome')
address_bar_wrapper = chrome_window['Google Chrome'].main.Edit.wrapper_object()



# loadLaunch = driver.find_element_by_link_text("Select from computer")
loadLaunch = driver.find_element_by_class_name("_acan._acap._acas")
loadLaunch = driver.find_elements_by_xpath("//BUTTON[text()='Select from computer']")
loadLaunch = driver.find_elements_by_tag_name("button")

loadLaunchX.send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png");

loadLaunchX = driver.find_elements_by_xpath('//*[@id="mount_0_0_Yx"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
loadLaunchX = driver.find_elements_by_xpath('//*[@id="mount_0_0_Yx"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')

loadLaunchX = driver.find_elements_by_partial_link_text('Select')
<button class="_acan _acap _acas" type="button">Select from computer</button>


app = Application().start("C:\\Program Files\\chromedriver_win32\\chromedriver.exe", timeout=10)


# app = app.connect()
dlg = app.top_window()
#  Navigate to window 
app = app.connect(title_re=' open ', class_name='#32770')
 

# need to load the actual file 
import pywinauto

pwa_app = pywinauto.application.Application()
w_handle = pywinauto.findwindows.find_windows()[0]
window = pwa_app.window_(handle=w_handle)
ctrl = window['Name']
ctrl.SetText(file)
ctrl = window['OK']
ctrl.Click()



# interact with the windows explorer pop up 
from pywinauto.application import Application
app = Application()
dlg = app.Chrome
app.connect(process=app.get_pid())  # connect to browser
dialog = app.top_window_()           # get active top window (Open dialog)
if not dialog.Edit.Exists():         # check if Edit field is exists
    time.sleep(1)                    # if no do again in 1 second (waiting for dialog after click)
    continue
dialog.Edit.TypeKeys('"{}"'.format(path))   # put file path
dialog['&OpenButton'].Click()               # click Open button


driver.activeElement().send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png");

s = driver.find_element_by_xpath("//input[@type='file']")
s.send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png");



driver.find_element_by_id("uploadfile_0")
loadLander = driver.find_element_by_class_name("_ab6-")
loadLander.send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png")

driver.find_element_by_class_name("_ab8w  _ab94 _ab97 _ab9h _ab9m _ab9p  _aba0 _abac")
driver.find_ele
# elem = driver.find_elements_by_xpath("//*[@type='submit']")#put here the content you have put in Notepad, ie the XPath
# button = driver.find_element_by_id('buttonID') //Or find button by ID.
# time.sleep(10)
# chrome_options.headless = True
# print(elem.get_attribute("class"))
driver.close()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')

WebDriver driver = new ChromeDriver();
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.quit()