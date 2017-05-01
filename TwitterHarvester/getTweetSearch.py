import sys,os,time
import json,jsonpickle
import tweepy
import couchdb
import TwitterSentiment
#log = open("tnsw.log", "a")
#sys.stdout = log

#f1=open('./output.txt', 'w+')
consumer_key = '6LI8WFTgasVJusVl68WVoJS5X'
consumer_secret = 'GJgYiiOKnNjhyGbsqHFfV4cDOUi7FzQ16DXHc9ca0bBFRi23qv'
access_token = '4506027074-Ics9Dy94Dvs1hxMMJ2OBRJzqGbc9VX1A61OPBFL'
access_secret = 'MWMagt2OsdXBRMVBBtq87OTbbx5NdVlQ55t4zQPWkKrOA'

def logPrint(s):
    f1=open('./output.txt', 'a')
    f1.write('\n'+s+"\n")
    f1.close()
#Ref: https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

#places = api.geo_search(query="AUSTRALIA", granularity="country")

#place_id = places[0].id
#print('AUSTRALIA id is: ',place_id)
#3f14ce28dc7c4566

#Database Setup
try:
    couch = couchdb.Server('http://115.146.93.140:5984/')
    db = couch['raw_tweets']
except:
    #print 'Database Connection Error'
    #print >> f1, "Database Connection Error"
    #f1.write('DB error')
    logPrint('DB Error')


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 
#Error handling
if (not api):
    #print ("Problem Connecting to API")
    #print >> f1, "Problem Connecting to API"
    #f1.write('API Error')
    logPrint('API Error')

#This is what we are searching for
ailist=['#AI',"artificial intelligence","#deeplearning","datascience",'#robots','robots','automation','#ArtificialIntelligence',
       '#bot','#bots','#ml','#iot','#tech','#analytics']
foodlist=['food','fitness food','#delicious','drink','eat','#coffee','beer','#foodie','#foodvision','#foodtruck','#eatingWell','#eatlocal','#foodparty']
politicslist = ['politics','immigration','migration','visa','#migration','#Australia','permanent migration program',"visa change",'sponsorship australia',
                  'labour party','liberal party','left wing','right wing','liberal party australia',
                  'politics australia','labour party australia','coalition party australia','australian labor party',
                  'australia politics','labour OR liberal','turnbull']
crimelist=['security Australia','robbed australia','safety australia','police','mugged australia','crime rate','crimes','justice Australia','terrorist australia',
'federal crime','robs australia','terrorist australia']

searchList=[ailist,foodlist,politicslist,crimelist]
#Search Config
maxTweets = 100000000000000
tweetsPerQry = 100
sinceId = None
max_id = -1L

# Search Criteria
lang='en'
geocode='-37.810279,144.962619,5000000mi'

searchListCount=0
totallistcount=0

maxList=len(searchList[totallistcount])
maxlistcount=len(searchList)
tweetCount = 0
#print("Downloading max {0} tweets".format(maxTweets))
#print >> f1, "Downloading max {0} tweets".format(maxTweets)
#f1.write('Downloading %d tweets' %maxTweets)
while tweetCount < maxTweets:
    
    if searchListCount>maxList-1:
        totallistcount+=1
        if totallistcount>maxlistcount-1:
            totallistcount=0
            maxlistcount=len(searchList[totallistcount])
        maxList=len(searchList[totallistcount][searchListCount])

    if totallistcount>maxlistcount-1:
        totallistcount=0
        maxlistcount=len(searchList[totallistcount])

    searchQuery=searchList[totallistcount][searchListCount]
    #print "Searching for: ",searchQuery
    #print >> f1, "Searching for: ",searchQuery
    #f1.write('Searching for %s' %searchQuery)
    logPrint('Searching for: '+str(searchQuery))
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode)#,)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            #print("No more tweets found, sleeping for 15 minutes")
            #print >> f1, "No more tweets found, sleeping for 15 minutes"
            #f1.write('No more tweets found, sleeping for 15 minutes')
            logPrint(' Sleeping 15 mins '+str(searchQuery))
            time.sleep(15*60)
            searchListCount+=1
            max_id = -1L
            sinceId = None
            continue
        
        for tweet in new_tweets:
            tweet_ = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
            clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
            sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
            tweet_['sentiment']=sentiment
            tweet_['searchQuery']=searchQuery
            db.save(tweet_)
        
        tweetCount += len(new_tweets)
        #print("Downloaded {0} tweets".format(tweetCount))
        #print >> f1, "Downloaded {0} tweets".format(tweetCount)
        #f1.write('Downloaded %d tweets' %tweetCount)
        logPrint(' Downloaded: '+str(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        #print("Tweepy Error")
        #print >> f1, "Tweepy Error"
        #f1.write('Tweepy Error')
        #fi.close()
        logPrint(' Tweepy Error ')
        time.sleep(15*60)
        searchListCount+=1
        max_id = -1L
        sinceId = None
        continue
        #break