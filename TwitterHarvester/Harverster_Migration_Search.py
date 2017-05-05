#!/usr/bin/python
import sys,os,time
import json,jsonpickle
import tweepy
import couchdb
import TwitterSentiment
import config
from config import logPrint


start_time = time.time()
consumer_key = config.CONSUMER_KEY_SAI
consumer_secret = config.CONSUMER_SECRET_SAI
access_token = config.ACCESS_TOKEN_SAI
access_secret = config.ACCESS_SECRET_SAI


#Ref: https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#places = api.geo_search(query="AUSTRALIA", granularity="country")
#place_id = places[0].id
#print('AUSTRALIA id is: ',place_id)
#3f14ce28dc7c4566

#Database Setup
#NSW
db=config.db_setup(config.SERVER_ADDRESS)
filename='HarNSW'

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    logPrint('API Error',filename)
    sys.exit()

#Search KeyWords
words=['immigration','migration','visa','#migration','#Australia','permanent migration program',
       "visa change",'sponsorship australia',"Skilled visa",
       "Visa","Visa law","Migration Australia","Immigrant",
       "Citizenship Australia","Permanent resident,","Visa subclass,",
       "visa 457","student visa Australia,","international students,",
       "partner visa","skilled migration","skilled occupation list,",
       "student migration","general skilled immigration,","migration,",
       "department of immigration","work visa","refugee","migration policy","visa policy"]


searchList=words
maxTweets = 100000000000000
tweetsPerQry = 100
sinceId = None
max_id = -1L

# Search Criteria
lang='en'
geocode='-37.810279,144.962619,10000mi'

searchListCount=20
maxlistcount=len(searchList)
tweetCount = 0
duplicates = 0
success = 0
while tweetCount < maxTweets:
    
    if searchListCount>maxlistcount-1:
        searchListCount=0

    searchQuery=searchList[searchListCount]
    logPrint('Searching for: '+str(searchQuery),filename)
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode)#,)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            
            if tweetCount%18000==0:
                time.sleep(15*60)
                logPrint(' Sleeping 15 mins: '+str(searchQuery),filename)
                start_time=time.time()  
            end = time.time()
            if (end-start_time)>14*60:
                time.sleep(15*60)
                logPrint(' Sleeping 15 mins: '+str(searchQuery),filename)
                start_time=time.time()
            searchListCount+=1
            max_id = -1L
            sinceId = None
            continue
        
        for tweet in new_tweets:
            tweet_ = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
            clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
            sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
            tweet_['sentiment']=sentiment
            tweet_['searchQuery']="migration"
            tweet_['_id']=tweet_['id_str']
            try:
                db.save(tweet_)
                success+=1
            except:
                duplicates+=1
                continue
                
        tweetCount += len(new_tweets)
        logPrint(' Added: '+str(success),filename)
        logPrint(' Skipped: '+str(duplicates),filename)
        max_id = new_tweets[-1].id

    except tweepy.TweepError as e:
        logPrint(str(e),filename)
        sys.exit()