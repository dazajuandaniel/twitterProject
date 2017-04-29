#!/usr/bin/python
import sys
import tweepy as tw
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb,json
import TwitterSentiment as ts
log = open("tnsw.log", "a")
sys.stdout = log

consumer_key = 'Rf6jmd167A0seBp8Nzg9w2LTs'
consumer_secret = 'cezVbuQna3A2mRo7dQCcjPk53qnTBSEFj1IZhxPRA3KaTrA5xR'
access_token = '853194331410227200-8qAydRzoIFelAP6ehk6gna4kBiOj6S8'
access_secret = 'nceGLJFyL31U9gHC7jVFk2RdwIHZ5G8RjjkHQe6HswNSj'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

try:
    couch = couchdb.Server('http://115.146.93.140:5984/')
    db = couch['raw_tweets']
except:
    print 'Database Connection Error'

class StdOutListener(StreamListener):
    def on_data(self, data):
        
        tweet = json.loads(data)
        #Adding Sentiment
        clean_tweet_text=ts.processTweet(tweet['text'])
        sentiment=ts.getSentiment(clean_tweet_text)
        tweet['sentiment']=sentiment
        db.save(tweet)
        #print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    stream = Stream(auth, l)    
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(locations=[141.157913,-38.022041,146.255569,-36.412349])
    stream.filter(locations=[147.921968,-35.889416,152.975679,-30.695000])