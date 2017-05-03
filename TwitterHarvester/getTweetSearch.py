#!/usr/bin/python
import sys,os,time
import json,jsonpickle
import tweepy
import couchdb
import TwitterSentiment
import config
from config import logPrint


consumer_key = '6LI8WFTgasVJusVl68WVoJS5X'
consumer_secret = 'GJgYiiOKnNjhyGbsqHFfV4cDOUi7FzQ16DXHc9ca0bBFRi23qv'
access_token = '4506027074-Ics9Dy94Dvs1hxMMJ2OBRJzqGbc9VX1A61OPBFL'
access_secret = 'MWMagt2OsdXBRMVBBtq87OTbbx5NdVlQ55t4zQPWkKrOA'


#Ref: https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
#places = api.geo_search(query="AUSTRALIA", granularity="country")
#place_id = places[0].id
#print('AUSTRALIA id is: ',place_id)
#3f14ce28dc7c4566

#Database Setup
db=config.db_setup(config.SERVER_ADDRESS)


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    logPrint('API Error')

#Search KeyWords
words=['#AI',"artificial intelligence","#deeplearning","datascience",'#robots','robots','automation','#ArtificialIntelligence',
       '#bot','#bots','#ml','#iot','#tech','#analytics',
       'food','fitness food','#delicious','drink','eat','#coffee','beer','#foodie','#foodvision','#foodtruck','#eatingWell','#eatlocal','#foodparty','restaurant','eating out',
       'beverage','chicken rice','pasta','indian food','food festival',
       'politics','immigration','migration','visa','#migration','#Australia','permanent migration program',"visa change",'sponsorship australia',
       'labour party','liberal party','left wing','right wing','liberal party australia',
       'politics australia','labour party australia','coalition party australia','australian labor party',
       'australia politics','labour OR liberal','turnbull',
       'security Australia','robbed australia','safety australia','police','mugged australia','crime rate','crimes','justice Australia','terrorist australia',
       'federal crime','robs australia','terrorist australia','jail sentence']


searchList=words
maxTweets = 100000000000000
tweetsPerQry = 100
sinceId = None
max_id = -1L

# Search Criteria
lang='en'
geocode='-37.810279,144.962619,10000mi'

searchListCount=0
maxlistcount=len(searchList)
tweetCount = 0
while tweetCount < maxTweets:
    
    if searchListCount>maxlistcount-1:
        searchListCount=0

    searchQuery=searchList[searchListCount]
    logPrint('Searching for: '+str(searchQuery))
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
            logPrint(' Sleeping 15 mins '+str(searchQuery))
            time.sleep(15*60)
            searchListCount+=1
            max_id = -1L
            sinceId = None
            continue
        
        for tweet in new_tweets:
            tweet_ = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
            clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
            sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
            tweet_['sentiment']=sentiment
            tweet_['searchQuery']=searchQuery
            db.save(tweet_)
        
        tweetCount += len(new_tweets)
        logPrint(' Downloaded: '+str(tweetCount))
        max_id = new_tweets[-1].id

    except tweepy.TweepError as e:
        logPrint(' Tweepy Error ')
        time.sleep(15*60)
        searchListCount+=1
        max_id = -1L
        sinceId = None
        continue