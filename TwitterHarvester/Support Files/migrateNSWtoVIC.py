import sys,os,time
import json
import couchdb
import TwitterSentiment

try:
    couch = couchdb.Server()
    db = couch['raw_tweets']
except:
    print 'Database Connection Error'

try:
    couchvic = couchdb.Server('http://115.146.93.140:5984/')
    dbvic = couchvic['raw_tweets']
except:
    print 'Database Connection Error'
count=0
for i in db:
    tweet=(db[i]['text'])
    clean_tweet_text=TwitterSentiment.processTweet(tweet)
    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    db[i]['sentiment']=sentiment
    dbvic.save(db[i])
    count+=1
print count
