#!/usr/bin/python
import sys, json
import couchdb
import tweepy as tw
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import TwitterSentiment as ts
import CheckKeyword as ck
import config
from config import logPrint

consumer_key = config.CONSUMER_KEY_SAI
consumer_secret = config.CONSUMER_SECRET_SAI
access_token = config.ACCESS_TOKEN_SAI
access_secret = config.ACCESS_SECRET_SAI

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

db = config.db_couch(config.NEWNODE_DB,config.SERVER_ADDRESS)
filename = 'StreamHarvester'

logPrint(' Starting ',filename)
class StdOutListener(StreamListener):
    def on_data(self, data):
        
        tweet = json.loads(data)
        #Adding Sentiment
        clean_tweet_text=ts.processTweet(tweet['text'])
        sentiment=ts.getSentiment(clean_tweet_text)
        tweet['sentiment']=sentiment
        tweet['_id']=tweet['id_str']
        topic = ck.checkMigration(clean_tweet_text)
        if topic=="migration":
            tweet['searchQuery']=topic
        try:
            db.save(tweet)
            logPrint(' Sucess ',filename)
            return True
        except:
            logPrint(' Fail ',filename)
            return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = StdOutListener()
    stream = Stream(auth, l)
    #Melbourne Area
    stream.filter(locations=[141.157913,-38.022041,146.255569,-36.412349])
    #Sydney Area
    #stream.filter(locations=[147.921968,-35.889416,152.975679,-30.695000])
