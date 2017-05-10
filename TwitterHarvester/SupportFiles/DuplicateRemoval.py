import couchdb
from config import logPrint

couch = couchdb.Server('http://dazaj:secret@115.146.93.140:5984/')

db = couch['raw_tweets']
db_new = couch['tweets_clean']

total_tweets=0
success=0
duplicates=0

for i in db.view('views/hasGeo'):#,reduce=True,group_level=1):
    doc=db[i.key]
    doc['_id']=doc['id_str']
    try:
        db_new.save(doc)
        success+=1
    except:
        duplicates+=1
        continue
    total_tweets+=1
    if total_tweets%50==0:
        print "Total Tweets so far: "+str(total_tweets) +"\n"+"Added to New: "+str(success),"duplicate"
    
