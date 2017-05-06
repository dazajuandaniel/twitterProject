#!/usr/bin/python
import sys,os,time
import ijson
import couchdb
import TwitterSentiment
import config
from config import logPrint

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
filename='tinyTwitter.json'
f = open(filename,"r")
objects = ijson.items(f,'item.json')
totalCount=0
added=0
for it in objects:
    doc=it
    doc['_id']=doc['id']
    clean_tweet_text=TwitterSentiment.processTweet(doc['text'])
    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    doc['sentiment']=sentiment
    for i in clean_tweet_text.split():
        if i in keywords:
            doc['searchQuery']=i
            continue    
    try:
        db.save(doc)
        totalCount+=1
        added+=1
    except:
        totalCount+=1
        continue

