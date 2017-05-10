#!/usr/bin/python
import os,time
import ijson,json
import couchdb
import TwitterSentiment
import config
from config import logPrint
import sys

#Words
keywords = ['immigration','migration','visa','migration','Australia','permanent migration program',
       "visa",'sponsorship',"skilled visa",
       "visa","visa law","migration","immigrant",
       "citizenship australia","resident,","visa subclass,",
       "visa 457","student visa Australia,","international students,",
       "partner visa","skilled migration","skilled occupation list,",
       "student migration","general skilled immigration,","migration,",
       "department of immigration","work visa","refugee","migration policy","visa policy","visa changes",
       "visa 189","migrant","migrant parents","skilled migration","skilled immigrants","skilled migrants",
       "skilled immigrant","sponsor visa","sponsorship visa","sol"]

#Open Big Twitter File
filename='bigTwitter.json'
f = open(filename,"r")
objects = ijson.items(f,'item.json')
totalCount=0
added=0
errors=0
db=config.db_aurin_setup(config.SERVER_ADDRESS)
print "Starting..."
for it in objects:
    totalCount+=1
    doc=json.loads(str(it))
    print type(doc)
    doc['_id']=doc['id_str']
    clean_tweet_text=TwitterSentiment.processTweet(doc['text'])
    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    doc['sentiment']=sentiment
    doc['sourceTweet']="bigTwitter"
    if totalCount<10:
        db.save(doc)
    for i in clean_tweet_text.split():
        if i in keywords:
            doc['searchQuery']=i
            try:
                db.save(doc)   
                added+=1
            except:
                errors+=1
                continue
            continue
    if totalCount%500==0:
        print "Total Tweets: ", totalCount
        print "Total Added: ",added
        print "Total Errors: ",errors


