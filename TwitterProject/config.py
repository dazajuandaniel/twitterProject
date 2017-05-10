import couchdb
from sys import exit



#JUAN
CONSUMER_KEY_JUAN = 'XqNOFK3tkWO3ueraq4WJgAbL8'
CONSUMER_SECRET_JUAN = 'KA79XONJOZL8WkBpZAuqkTjDxRhiT7KGf16x2SLTCFfqSpTnoG'
ACCESS_TOKEN_JUAN = '140966719-NrfyS8phWv3pJAwCQkqoZESAWTQo6AQzfVVYH1Rf'
ACCESS_SECRET_JUAN = 'Efi3AuiHq1DTIAfucEFt7SgCZ8rFHsF4Cibk1RJNC95Rt'

#WEN
CONSUMER_KEY_WEN = 'Rf6jmd167A0seBp8Nzg9w2LTs'
CONSUMER_SECRET_WEN = 'cezVbuQna3A2mRo7dQCcjPk53qnTBSEFj1IZhxPRA3KaTrA5xR'
ACCESS_TOKEN_WEN = '853194331410227200-8qAydRzoIFelAP6ehk6gna4kBiOj6S8'
ACCESS_SECRET_WEN = 'nceGLJFyL31U9gHC7jVFk2RdwIHZ5G8RjjkHQe6HswNSj'

#JEN
CONSUMER_KEY_JUN = '6LI8WFTgasVJusVl68WVoJS5X'
CONSUMER_SECRET_JUN = 'GJgYiiOKnNjhyGbsqHFfV4cDOUi7FzQ16DXHc9ca0bBFRi23qv'
ACCESS_TOKEN_JUN = '4506027074-Ics9Dy94Dvs1hxMMJ2OBRJzqGbc9VX1A61OPBFL'
ACCESS_SECRET_JUN = 'MWMagt2OsdXBRMVBBtq87OTbbx5NdVlQ55t4zQPWkKrOA'

#SAI
CONSUMER_KEY_SAI='KgUYNFkNqmP9DeNVj9gurL6pV'
CONSUMER_SECRET_SAI='vLjsRYnwYvLKqQAuiQXgjHDWE0RJ9AqYoWU3H2yzPkOfg6nBy1'
ACCESS_TOKEN_SAI='150621173-8wZG1ShJh3Us4II2hhHKISwSSpPSKuE4pGwgHvdT'
ACCESS_SECRET_SAI='mLB3fsqsNXVZR8MTXOOVWX2HUxAy3eVM1VLWSufYLVUCO'

#MICHAEL
CONSUMER_KEY_MICHAEL='lsjopDJ77AUDGaGDw3Nggqm9R'
CONSUMER_SECRET_MICHAEL='esepC8AmVqqnLdSSEL6N1dMrB1z9TIscbEviQQzrW5JzqbBFum'
ACCESS_TOKEN_MICHAEL='1638515630-VZn3TJDqAGOdh29o6nB4PhrvVvKHKWeRYUTmAM3'
ACCESS_SECRET_MICHAEL='q1HXBKn8Hn9eT1jxBIIChHtX5dcTCBBptyRaqCJsiJ8ko'

USER='dazaj'
PASS='secret'

#Constants
SERVER_ADDRESS='http://'+USER+":"+PASS+"@"+'115.146.93.140:5984/'
#Special Print
def logPrint(s,name):
    f1=open('./'+name+'.txt', 'a')
    f1.write('\n'+s+"\n")
    f1.close()
filename='configFile'
#Database Setup
def db_setup(address=''):
    if address=='':
        address='localhost:5984/'
        try:
            couch = couchdb.Server('http://'+USER+":"+PASS+"@"+address)
            db = couch['raw_tweets']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    else:
        try:
            couch = couchdb.Server(SERVER_ADDRESS)
            db = couch['raw_tweets']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    return db

def db_clean_setup(address=''):
    if address == '':
        address = 'localhost:5984/'
        try:
            couch = couchdb.Server('http://'+USER+":"+PASS+"@"+address)
            db = couch['tweets_clean']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    else:
        try:
            couch = couchdb.Server(SERVER_ADDRESS)
            db = couch['tweets_clean']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    return db

def db_aurin_setup(address=''):
    if address == '':
        address = 'localhost:5984/'
        try:
            couch = couchdb.Server('http://'+USER+":"+PASS+"@"+address)
            db = couch['coordinates_aurin']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    else:
        try:
            couch = couchdb.Server(SERVER_ADDRESS)
            db = couch['coordinates_aurin']
            logPrint('Database Success',filename)
        except:
            logPrint('Database Connection Error',filename)
            exit()
    return db



