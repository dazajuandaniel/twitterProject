import couchdb


#Database Setup
def db_setup():
    try:
        couch = couchdb.Server('http://115.146.93.140:5984/')
        db = couch['raw_tweets']
    except:
        print 'Database Connection Error'
    return db
