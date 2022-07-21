# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:46:02 2022

@author: Pete

python script to accomplish the following
> get tweets from Twitter User Profiles
> Get Screenshots for the applicable tweets
> Save the tweets as images 
> Post to Instagram (currently will just be texted to a phone #)

"""


# load required packages and set directories 
# ================================================
import os 
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import tweepy
import json 
import pandas as pd 
from datetime import datetime
import io 
import pyppeteer # pip install pyppeteer
import asyncio
import nest_asyncio
nest_asyncio.apply()
import pytesseract
from pytesseract import pytesseract
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import time
from PIL import Image, ImageDraw # pip install Pillow
from email.mime.base import MIMEBase
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
# packages required for web scraping: 
# need to download a seperate driver here: https://www.geeksforgeeks.org/click-button-by-text-using-python-and-selenium/
# its called "chrome driver" instead of just "chrome" 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
# packages required for connecting to a random proxy 
# documentation for proxy_randomizer available here: https://pypi.org/project/proxy-randomizer/
from proxy_randomizer import RegisteredProviders # pip install proxy_randomizer
from proxy_randomizer.proxy import Anonymity
import random

# directory 
wd = "C:\\Users\\Pete\\Documents\\GitHub\\percySandbox\\twitterScreenshots\\buffaloBills"
archivedTweetsWd = "C:\\Users\\Pete\\Documents\\Projects\\Twitter Screenshots\\Buffalo Bills\\alreadyProcessedFiles"
screenshotWd = wd + "\\screenshots"
os.chdir(wd)
print('Currently working in: ' + os.getcwd())
# get datetime 
sysDate = datetime.now()
fmtSysDate = sysDate.strftime('%Y%m%d')
fmtSysDatetime = sysDate.strftime('%Y%m%d_%H%M%S')

# define secrets 
# ================================================
pwdPath = 'C:\\Users\\Pete\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
# twitter 
twitterConsumerKey = pwdDf[['personalTwitter']].filter(like = 'consumerKey', axis = 0).to_string(index=False, header= False).strip()
twitterConsumerSecret = pwdDf[['personalTwitter']].filter(like = 'consumerSecret', axis = 0).to_string(index=False, header= False).strip()
twitterAccessToken = pwdDf[['personalTwitter']].filter(like = 'accessTokenKey', axis = 0).to_string(index=False, header= False).strip()
twitterAccessTokenSecret = pwdDf[['personalTwitter']].filter(like = 'accessTokenSecret', axis = 0).to_string(index=False, header= False).strip()
# gmail
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()
toEmail = "4126805149@mms.att.net"
fromEmail = emailUser
# instagram
igUserName = pwdDf[['instagram_billsTweets']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
igPassword = pwdDf[['instagram_billsTweets']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()

# connect to twitter and sweep tweets 
# ================================================
auth = OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
api = tweepy.API(auth)

# just to check if we're connected, can delete later 
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
    
    
# grab the tweet id, url and timestamp for each tweet currently on the web 
j = 0 
dfTwitterApi = pd.DataFrame(columns = ['tweetId', 'url', 'createdAt'])
for tweet in tweepy.Cursor(api.user_timeline,id='buffalobills').items(100):
    j = j+ 1
    # print(j)
    print('Line # ' + str(j) + ':')
    print(tweet.id_str)
    print('Url for Line # ' + str(j) + ':')
    tweetId = tweet.id_str
    tweetUrl = 'https://twitter.com/twitter/statuses/' + tweetId
    print(tweetUrl)
    tweetCreatedAt = tweet.created_at
    print(tweetCreatedAt)
    dfTwitterApi = dfTwitterApi.append(
        pd.DataFrame(
            [[tweetId, tweetUrl, tweetCreatedAt]]
            , columns = ['tweetId', 'url', 'createdAt']
            )
        )

# clean up the api dataframe 
dfTwitterApi['createdAt'] = pd.to_datetime(dfTwitterApi['createdAt'])


# compare to the "already processed file"
# temp - creating the original "already processed file"
# apFileNameNew = 'alreadyProcessed_' + fmtSysDatetime + '.csv'
# apFilePathNew = wd + "\\alreadyProcessedFiles\\" + apFileNameNew
# dfTwitterApi.to_csv(apFilePathNew , index = False)


# read in the "already processed" records
apFileNameLast = sorted(os.listdir(archivedTweetsWd), reverse = True)[0]
apPathNameLast = archivedTweetsWd + '//' + apFileNameLast
dfAlreadyProcessed = pd.read_csv(apPathNameLast)
dfAlreadyProcessed['tweetId'] = dfAlreadyProcessed['tweetId'].astype(str)
# cross reference already processed against the api data frame 
dfTwitterApiFilter = dfTwitterApi.merge(dfAlreadyProcessed , left_on = 'tweetId' , right_on = 'tweetId', how = 'left' )
dfTwitterApiFilter = dfTwitterApiFilter[dfTwitterApiFilter.url_y.isnull()]
# rename the columns and drop the extra ones 
dfTwitterApiFilter = dfTwitterApiFilter.drop(columns = ['url_y', 'createdAt_y']) 
dfTwitterApiFilter = dfTwitterApiFilter.rename(columns={"url_x": "url", "createdAt_x":"createdAt"})

# filter down to the oldest tweet that has not been processed yet 
dfTwitterApiFinal = dfTwitterApiFilter.sort_values(by = 'createdAt').head(1)

# if dfTwitterApiFinal has no rows, then skip the rest of the steps and say "all caught up" 
if len(dfTwitterApiFinal) == 0:
    print('We\'re all caught up!!')
else:   
    inProcessId = dfTwitterApiFinal[["tweetId"]].to_string(index=False, header= False).strip()
    inProcessUrl = dfTwitterApiFinal[["url"]].to_string(index=False, header= False).strip()
    inProcessCreatedAt = dfTwitterApiFinal[["createdAt"]].to_string(index=False, header= False).strip()
    inProcessCreatedAtDt = pd.to_datetime(inProcessCreatedAt)
    inProcessCreatedAtFormat = inProcessCreatedAtDt.strftime('%B %d, %Y at %I:%M %p')
    screenshotFileName = 'screenshot.png'
    # gonna use for the message Text 
    
    # grab screenshot and save to local directory 
    # ================================================
    # change working directory 
    os.chdir(screenshotWd)
    # image 1 
    async def main():
       #  browser = await pyppeteer.launch()
        browser = await pyppeteer.launch(headless=True, executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' )
        page = await browser.newPage()
        await page.setViewport({"width": 1600, "height": 900})
        await page.goto(inProcessUrl)
        #await page.goto(inProcessUrl, {"waitUntil" : "networkidle0"})
        time.sleep(7)
        await page.screenshot({'path': screenshotFileName, 'fullPage':True})
        await browser.close()
    
    asyncio.get_event_loop().run_until_complete(main())
    
    # crop the screenshot to the appropriate size 
    # ================================================
    fullImage = Image.open(screenshotWd + '\\' + screenshotFileName)
    width, height = fullImage.size 
    # === attempting to convert image to grayscale to better read the data from 
    import cv2
    import numpy as np
    fullImageCv = cv2.imread(screenshotFileName)
    gray = cv2.cvtColor(fullImageCv, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
    # cv2.imshow('sharpen', sharpen)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]    
    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    data2 = pytesseract.image_to_string(fullImageCv, lang='eng', config='--psm 6')
    print(data)
    # === end of attempt
    # fullImageResults = pytesseract.image_to_data(fullImage)
    fullImageResults = pytesseract.image_to_data(thresh)
    fullImageResults2 = pytesseract.image_to_data(fullImageCv)
    # fullImageResults2 = pytesseract.image_to_data(fullImage)
    fullImageResultsDf = pd.read_csv(io.StringIO(fullImageResults), sep = '\t', engine = "python", encoding = 'utf-8', error_bad_lines=False)
    fullImageResultsDf2 = pd.read_csv(io.StringIO(fullImageResults2), sep = '\t', engine = "python", encoding = 'utf-8', error_bad_lines=False)
    # fullImageResultsDf2 = pd.read_csv(io.StringIO(fullImageResults2), sep = '\t', engine = "python", encoding = 'utf-8', error_bad_lines=False)
    # find the location of the word "Retweet" [Nth character]
    fullImageResultsDfLite = fullImageResultsDf[fullImageResultsDf.text.notnull()]
    fullImageResultsDfLite2 = fullImageResultsDf2[fullImageResultsDf2.text.notnull()]
    # sometimes the image ai app messes up retweets, so add any close variations below: 
    # 	Retweets
    searchableStrings = ['Retweets', 'Retwests']
    fullImageResultsDfLite = fullImageResultsDfLite[fullImageResultsDfLite['text'].str.contains('|'.join(searchableStrings))]
    fullImageResultsDfLite2 = fullImageResultsDfLite2[fullImageResultsDfLite2['text'].str.contains('|'.join(searchableStrings))]
    if len(fullImageResultsDfLite) == 0:
        retweetsTop = int(fullImageResultsDfLite2['top'].to_string(index=False, header= False).strip())
    else:
        retweetsTop = int(fullImageResultsDfLite['top'].to_string(index=False, header= False).strip())
    # then, crop at that location + 10 or so 
    # need to rework the specific numbers 
    left = 0
    left =  445
    top = 0 
    top = 45
    right = width - 560
    bottom = retweetsTop - 25 # 25 was a good number to account for the twitter spacing 
    croppedImage = fullImage.crop((left, top, right, bottom))
    croppedImage.save(screenshotWd +'\\screenshot_cropped.png',optimize=True,quality=100)
    newFile = 'screenshot_cropped.png'
    newFilePad = 'screenshot_padding.png'
    
    # pad the screenshot to have some borders [aka will square enough for ig]
    # ================================================
    # define how extreme we can get with the width or height of our picture
    # using this as my source, but need to stay current:
    # https://colorlib.com/wp/size-of-the-instagram-picture/
    # Instagram Landscape (horizontal) Photo	1080 X 608 (1.91:1 ratio)
    # Instagram Portrait	1080 x 1350 (4:5 ratio)
    landscapeRatio = (1 / 1.91) 
    portraitRatio = (4 / 5)
    
    topImage = croppedImage
    widthTop, heightTop = topImage.size 
    if widthTop > heightTop:
        orientation = 'Landscape'
        # check if the current dimensions meet the min 
        if heightTop < landscapeRatio * widthTop:
            print('image isnt square enough ')
            # create background shape (white color)
            widthRect, heightRect = widthTop, (landscapeRatio * widthTop)
            shape = [(0, 0), (widthRect, heightRect)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
            rectImage = Image.new("RGB", (widthRect, int(heightRect)))
            # create rectangle image
            rectImageDraw = ImageDraw.Draw(rectImage)  
            rectImageDraw.rectangle(shape, fill ="white")
            # rectImage.show()
            # place the top image 
            rectImageMerge = rectImage
            # will need to use the following equation for landscape mode .... int((widthRect - widthTop) / 2)
            rectImageMerge.paste(topImage, (0, int((heightRect - heightTop) / 2)), topImage)
            # rectImageMerge.show()
            rectImageMerge.save(screenshotWd +'\\screenshot_padding.png',optimize=True,quality=100)
            # save the image as "screenshot_padding.png"
        else: 
            print('image is square enough')
            rectImageMerge = Image.open(screenshotWd + '\\' + newFile)
            rectImageMerge.save(screenshotWd +'\\screenshot_padding.png',optimize=True,quality=100)
            # save the image as "screenshot_padding.png"
    else:
        orientation = 'Portrait'
        if widthTop < portraitRatio * heightTop:
            print('image isnt square enough ')
            # create background shape (white color)
            widthRect, heightRect = (portraitRatio * heightTop), heightTop
            shape = [(0, 0), (widthRect, heightRect)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
            rectImage = Image.new("RGB", (int(widthRect), heightRect))
            # create rectangle image
            rectImageDraw = ImageDraw.Draw(rectImage)  
            rectImageDraw.rectangle(shape, fill ="white")
            # rectImage.show()
            # place the top image 
            rectImageMerge = rectImage
            # will need to use the following equation for landscape mode .... int((widthRect - widthTop) / 2)
            rectImageMerge.paste(topImage, (int((widthRect - widthTop) / 2), 0), topImage)
            # rectImageMerge.show()
            rectImageMerge.save(screenshotWd +'\\screenshot_padding.png',optimize=True,quality=100)
            # save the image as "screenshot_padding.png"
        else: 
            print('image is square enough')     
            rectImageMerge = Image.open(screenshotWd + '\\' + newFile)
            rectImageMerge.save(screenshotWd +'\\screenshot_padding.png',optimize=True,quality=100)
            # save the image as "screenshot_padding.png"
        
    
    # post the padded picture to instagram 
    # =========================================================================
    # generate a list of random proxies and pick one 
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    rp = RegisteredProviders()
    rp.parse_providers()
    # generate a list of "anonymous" proxies
    anonymous_proxies = list(
        filter(lambda proxy: proxy.anonymity == Anonymity.ANONYMOUS, rp.proxies)
    )
    print(f"filtered proxies: {anonymous_proxies}")
    # create a dataframe of only the us proxies 
    ipDf = pd.DataFrame({'fullString':[], 'ip':[]})
    for i in anonymous_proxies:
        currentProxy = i.get_proxy()
        print(type(currentProxy))
        ipDf = ipDf.append(pd.DataFrame({'fullString':[str(i)], 'ip':[i.get_proxy()]}))
        print('added 1 row to the df')
        # if 'United States' in str(i):
            # print(i)
            # print(currentProxy)
            # ipDf = ipDf.append(pd.DataFrame({'fullString':[str(i)], 'ip':[i.get_proxy()]}))
            # print('added 1 row to the df')

    randoPick = [random.randint(1, 10)][0]
    print(randoPick)
    # select the proxy to use 
    ipDfActive = ipDf.iloc[randoPick-1]
    print(ipDfActive[1])
    ipActive = ipDfActive[1]
    # confirgure selenium connection setting 
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = ipActive
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
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
    
    
    # select the ("new post" button )
    # ----------------------------------------------------------------
    newPostButtonResults = driver.find_elements_by_css_selector("[aria-label='New post']")
    for i in newPostButtonResults:
        print(i.text)
        newPostButton = i 
    
    newPostButton.click()
    time.sleep(1)
    
    # attempt to run the file load 
    # ----------------------------------------------------------------
    inputFormResults = driver.find_elements_by_css_selector('input')
    for i in inputFormResults:
        print(i.text)
        inputForm = i
    
    # inputForm.send_keys("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png")
    igLoadFileName = screenshotWd +'\\screenshot_padding.png'
    inputForm.send_keys(igLoadFileName)
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
    # actions.send_keys('My caption <3')
    actions.send_keys(inProcessUrl)
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


    # send a text to pete containing the image and caption 
    # ================================================
    # will eventually be an instagram post 
    captionText = ('Posted to Twitter at ' 
                   + inProcessCreatedAtFormat + '. See more at the link below.\n\n'
                   + inProcessUrl + '\n\nTweetId: ' + tweetId)
    
    # send email 
    msg = MIMEMultipart("alternative")
    # msg["Subject"] = "SubjectLine"
    msg["From"] = fromEmail
    msg["To"] = toEmail
    bodyMime = MIMEText(captionText)
    msg.attach(bodyMime)
    # Open PDF file in binary mode
    with open(newFilePad, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {newFilePad}",
    )
    
    # Add attachment to message and convert message to string
    msg.attach(part)
    
    # send the actual note
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(emailUser, emailPw)
    server.sendmail(fromEmail, toEmail, msg.as_string())
     
    # save the file as the newest "already processed" 
    dfAlreadyProcessedUpdate = pd.concat([dfAlreadyProcessed, dfTwitterApiFinal])
    apFileNameNew = 'alreadyProcessed_' + fmtSysDatetime + '.csv'
    apFilePathNew = archivedTweetsWd + '\\' + apFileNameNew
    # apFilePathNew = wd + "\\alreadyProcessedFiles\\" + apFileNameNew
    dfAlreadyProcessedUpdate.to_csv(apFilePathNew , index = False)
    
    # delete the screenshots 
    os.remove(screenshotWd +'\\' + 'screenshot.png')
    os.remove(screenshotWd +'\\' + 'screenshot_cropped.png')
    os.remove(screenshotWd +'\\' + 'screenshot_padding.png')
    # delete anything older than the last 30 tweets
    # gonna delete the last 3 or so for now 
    # nned to rework the below 
    filesToKeep = sorted(os.listdir(archivedTweetsWd), reverse = True)[0:30]
    for i in sorted(os.listdir(archivedTweetsWd), reverse = True):
        print(i)
        if i in filesToKeep:
            print('No need to delete!')
        else:
            os.remove(archivedTweetsWd + '\\' + i)
    
