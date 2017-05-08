import couchdb
import TwitterSentiment
import pandas as pd
import config

dbAurin=config.db_aurin_setup(config.SERVER_ADDRESS)
dbTweets=config.db_clean_setup(config.SERVER_ADDRESS)

#Get Tweets that have Suburb and Sentiment data About Migration
suburbList=[]
suburbSentiment=[]
suburbCount=[]
count=0
for i in db_new.view('view/MigrationSuburbSent',reduce=True,group_level=2):
    suburbList.append(int(i.key[0]))
    suburbSentiment.append((i.key[1]))
    suburbCount.append(int(i.value))

#Create Dataframe
d = {'suburb' : suburbList,
     'sentiment' : suburbSentiment,
    'count':suburbCount}
data=pd.DataFrame(d)

#Get Aurin Data to Correlate
aurin={}
for i in db_2.view('views/allDocs'):
    aurin[i.key]=i.value

#Append Aurin Data to Dataframe
name=[]
tafe=[]
uni=[]
high=[]
income=[]
for i in data['suburb']:
    name.append(aurin[str(i)]['name'])
    tafe.append(aurin[str(i)]['tafe'])
    uni.append(aurin[str(i)]['uni'])
    high.append(aurin[str(i)]['highschool'])
    income.append(aurin[str(i)]['income'])

data['Name']=name
data['Tafe']=tafe
data['University']=uni
data['high']=high
data['income']=high