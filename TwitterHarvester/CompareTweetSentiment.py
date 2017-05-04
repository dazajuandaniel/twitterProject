import AFINNSentiment
import config

db=config.db_setup(config.SERVER_ADDRESS)

count=0
for i in db.view('views/hasGeo'):
    if count<1000:
        id=i.id
        doc=db.get(id)
        tweet=doc['text']
        sentiment_value=AFINNSentiment.sentiment(tweet)
        sentiment=AFINNSentiment.getSentiment(sentiment_value)
        doc['sentimentAFINN']=sentiment
        db[id]=doc
        count+=1
    




