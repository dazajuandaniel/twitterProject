import couchdb
import simplejson as json
#import shapely.geometry 

from flask import Flask
from flask import render_template
import json


app = Flask(__name__)





@app.route('/sentiPieChart')
def hello():
     server = couchdb.Server('http://dazaj:secret@115.146.93.140:5984')
     db = server['tweets_clean']
     v = db.view('_design/view/_view/TweetsbySentiment', group=True)
     d = {}
     sum = 0 
     for row in list(v):
         d[row.key] = row.value
     for keys,values in d.items():
         sum+=values
     for keys,values in d.items():
         d[keys] = values/sum*100
     j = json.dumps([{'name': k, 'y': v} for k,v in d.items()], indent=4)
     return render_template('sentiPieChart.html', data=j)

@app.route('/sentiHour')
def hello2():
     server = couchdb.Server('http://dazaj:secret@115.146.93.140:5984')
     db = server['tweets_clean']
     v = db.view('_design/view/_view/TweetsbyHour', group=True)
     tempd = {'name':'tweetnumber','data':[]}
     d = [] 
     for row in list(v):
         d.append(row.value)
     tempd['data'] = d
     j = json.dumps([tempd],indent=4)
     return render_template('sentiHour.html', data=j)

@app.route('/sentiHourSenti')
def hello3():
     server = couchdb.Server('http://dazaj:secret@115.146.93.140:5984')
     db = server['tweets_clean']
     v = db.view('_design/view/_view/TweetsbyHourSentiment', group=True)
     td1 = {'name':'Negative','data':[]}
     td2 = {'name':'Neutral','data':[]}
     td3 = {'name':'Positive','data':[]}
     for row in list(v):
         if(row.key[1] == 'Negative'):
                     td1['data'].append(row.value)
         elif(row.key[1] == 'Neutral'):
                     td2['data'].append(row.value)
         else: 
             td3['data'].append(row.value)

     j = json.dumps([td1,td2,td3],indent=4)
     return render_template('sentiHourSenti.html', data=j)







@app.route('/immigrationEdu')
def hello4():
    server = couchdb.Server('http://dazaj:secret@115.146.93.140:5984')
    db = server['twitter_analysis']  
    db2 =  server['twitter_analysis2']  

    for docid in db:
        doc = db[docid]
        tweettext = doc['docs']
        str = json.dumps(tweettext)

    for docid2 in db2:
        doc2 = db2[docid2]
        tweettext2 = doc2['docs']
        str2 = json.dumps(tweettext2)

    return render_template('immigrationEdu.html', data=str,data2=str2)





@app.route('/immigrationMoney')
def hello5():
    server = couchdb.Server('http://dazaj:secret@115.146.93.140:5984')
    db = server['twitter_analysis3']    
    for docid in db:
        doc = db[docid]
        tweettext = doc['docs']
        str = json.dumps(tweettext)
        return render_template('immigrationMoney.html', data=str)
        


@app.route('/index')
def hello6():
    return render_template('index.html', data=str)


     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)









