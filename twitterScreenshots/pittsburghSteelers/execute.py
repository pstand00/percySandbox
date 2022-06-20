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
# directory 
wd = "C:\\Users\\Pete\\Documents\\GitHub\\percySandbox\\twitterScreenshots\pittsburghSteelers"
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
# eventually [instagram]

# connect to twitter and sweep tweets 
# ================================================
auth = OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
api = tweepy.API(auth)

# just to check if we're connected, can delete later 
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
    
    
# grab the tweet id, url and timestamp for each tweet currently on the web 
j = 0 
dfTwitterApi = pd.DataFrame(columns = ['tweetId', 'url', 'createdAt'])
for tweet in tweepy.Cursor(api.user_timeline,id='steelers').items(250):
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
apFileNameLast = sorted(os.listdir(wd + "\\alreadyProcessedFiles\\"), reverse = True)[0]
apPathNameLast = wd + "\\alreadyProcessedFiles\\" + apFileNameLast
dfAlreadyProcessed = pd.read_csv(apPathNameLast)

# cross reference already processed against the api data frame 


    