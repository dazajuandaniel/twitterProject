import couchdb
import TwitterSentiment



def logPrint(s):
    f1=open('./output.txt', 'a')
    f1.write('\n'+s+"\n")
    f1.close()

try:
    couch = couchdb.Server('http://115.146.93.140:5984/')
    db = couch['raw_tweets']
    print "Ok DB"
except:
    logPrint('DB Error')

count=0
#Loop to get without Sentiemnt
for row in db.view('views/HasNoSentiment'):
    id=row.id
    doc=db.get(id)
    tweet=doc['text']
    clean_tweet_text=TwitterSentiment.processTweet(tweet)
    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    doc['sentiment']=sentiment
    db[id]=doc
    count+=1
logPrint("Total Adjusted: "+str(count))
    
