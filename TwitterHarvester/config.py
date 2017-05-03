import couchdb

SERVER_ADDRESS='http://115.146.93.140:5984/'


#Database Setup
def db_setup(address):
    try:
        couch = couchdb.Server(address)
        db = couch['raw_tweets']
    except:
        print 'Database Connection Error'
    return db

#Special Print
def logPrint(s):
    f1=open('./output.txt', 'a')
    f1.write('\n'+s+"\n")
    f1.close()
