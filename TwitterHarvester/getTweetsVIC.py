#!/usr/bin/python
import sys
import tweepy as tw
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb,json
import TwitterSentiment as ts
import config

consumer_key = 'XqNOFK3tkWO3ueraq4WJgAbL8'
consumer_secret = 'KA79XONJOZL8WkBpZAuqkTjDxRhiT7KGf16x2SLTCFfqSpTnoG'
access_token = '140966719-NrfyS8phWv3pJAwCQkqoZESAWTQo6AQzfVVYH1Rf'
access_secret = 'Efi3AuiHq1DTIAfucEFt7SgCZ8rFHsF4Cibk1RJNC95Rt'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

db=config.db_setup('')

class StdOutListener(StreamListener):
    def on_data(self, data):
        
        tweet = json.loads(data)
        #Adding Sentiment
        clean_tweet_text=ts.processTweet(tweet['text'])
        sentiment=ts.getSentiment(clean_tweet_text)
        tweet['sentiment']=sentiment
        db.save(tweet)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = StdOutListener()
    stream = Stream(auth, l)    
    stream.filter(locations=[141.157913,-38.022041,146.255569,-36.412349])
    #stream.filter(locations=[147.921968,-35.889416,152.975679,-30.695000])