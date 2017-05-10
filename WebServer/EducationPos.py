
import json
import requests
import pandas as pd
import config
import numpy as np 
headers = {"Content-Type":"application/json"}

#DB Connection
db_new=config.db_clean_setup(config.SERVER_ADDRESS)
db_2=config.db_aurin_setup(config.SERVER_ADDRESS)
#Get Documents with Migration Topic and Suburb values
suburbList=[]
suburbSentiment=[]
suburbCount=[]
count=0
for i in db_new.view('view/MigrationSuburbSent',reduce=True,group_level=2):
    suburbList.append(int(i.key[0]))
    suburbSentiment.append((i.key[1]))
    suburbCount.append(int(i.value))
#Create DataFrame
d = {'suburb' : suburbList,
     'sentiment' : suburbSentiment,
    'count':suburbCount}
data=pd.DataFrame(d)
#Get Suburb Data from Couchdb
aurin={}
for i in db_2.view('views/allDocs'):
    aurin[i.key]=i.value

#Add Aurin Data to Dataset
name=[]
tafe=[]
uni=[]
high=[]
income=[]
employment=[]
for i in data['suburb']:
    name.append(aurin[str(i)]['name'])
    tafe.append(aurin[str(i)]['tafe'])
    uni.append(aurin[str(i)]['uni'])
    high.append(aurin[str(i)]['highschool'])
    income.append(aurin[str(i)]['income'])
    employment.append(aurin[str(i)]['employmentratio'])

data['Name']=name
data['Tafe']=tafe
data['University']=uni
data['high']=high
data['income']=income
data['employment']=employment

#Aggregate Data
groupedCount=data.groupby(['suburb']).count().reset_index()
groupedSum=data.groupby(['suburb']).sum().reset_index()

#Add Aggregate to Data. This aggregate data is collected to find out the total number of tweets per suburb per sentiment
#and to see if suburb contained all three sentiments (Positive, Neutral & Negative)
found=False
value={}
valuesum={}
index=[]
for i in range(len(data['suburb'])):
    for j in range(len(groupedCount['suburb'])):
        if data['suburb'][i]==groupedCount['suburb'][j]:
            value[data['suburb'][i]]=groupedCount['count'][j]

for i in range(len(data['suburb'])):
    for j in range(len(groupedSum['suburb'])):
        if data['suburb'][i]==groupedSum['suburb'][j]:
            valuesum[data['suburb'][i]]=groupedSum['count'][j]

#Attach to Data
array=[]
arraysum=[]
for i in range(len(data)):
    array.append(value[data['suburb'][i]])
    arraysum.append(valuesum[data['suburb'][i]])
data['totCount']=array
data['totSum']=arraysum

#Get Percetange of Each sentiment
gr=data.groupby(['suburb','Name','sentiment']).agg({'count': 'sum'})
gr_per=gr.groupby(level=0).apply(lambda x:x / float(x.sum()))
gr_per_=gr_per.reset_index()

perc=[]
for i in range(len(data)):
    for j in range(len(gr_per_)):
        if data['suburb'][i]==gr_per_['suburb'][j] and data['sentiment'][i]==gr_per_['sentiment'][j]:
            perc.append(gr_per_['count'][j])
            break
data['Percentage']=perc
dataSorted=data.sort_values(by=['totSum','Name','totCount'],ascending=False).reset_index()
dataSorted=data.sort_values(by=['totSum','Name','totCount','University'],ascending=False).reset_index()

negativeSet=dataSorted[(dataSorted['Percentage']>.25) & (dataSorted['sentiment']=="Negative")].head()
negativeSet=negativeSet.sort_values(by='University',ascending=False).reset_index()

positiveSet=dataSorted[(dataSorted['sentiment']=="Positive")].head()
positiveSet=positiveSet.sort_values(by='University',ascending=False).reset_index()

td1 = {'type':'column','name':'TAFE','data':[]}
td2 = {'type':'column','name':'UNIVERSITY','data':[]}
td3 = {'type':'column','name':'HIGH SCHOOL','data':[]}

total = [1,2,3,4,5]
t = [0,0,0]
i = 0
for key,values in positiveSet.items():
    if(key=='Tafe'):
        a1 = np.array(values, dtype=pd.Series)
        for k in a1:
         td1['data'].append(k)  
         t[0] += k
         total[i] += k
         i += 1
        i = 0
    elif(key=='University'):
        a2 = np.array(values, dtype=pd.Series)
        for k in a2:
         td2['data'].append(k)  
         t[1] += k
         total[i] += k
         i += 1
        i = 0
    elif(key=='high'):
        a3 = np.array(values, dtype=pd.Series)
        for k in a3:
         td3['data'].append(k)  
         t[2] += k
         total[i] += k
         i += 1
        i = 0 

tdpie = {
        'type': 'pie',
        'name': 'Total consumption',
        'data': [{
            'name': 'TAFE',
            'y': t[0],
            'color': 'red'
        }, {
            'name': 'UNIVERSITY',
            'y': t[1],
            'color': 'blue' 
        }, {
            'name': 'HIGH SCHOOL',
            'y': t[2],
            'color': 'green'
        }],
        'center': [120, 40],
        'size': 100,
        'showInLegend': 'false',
        'dataLabels': {
            'enabled': 'false'
        }
    }


j = json.dumps([td1,td2,td3,tdpie],indent=4)
print(j)