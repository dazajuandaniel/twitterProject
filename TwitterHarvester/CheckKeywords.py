import TwitterSentiment
import config

#Search KeyWords
WORDS=['immigration','migration','visa','#migration','permanent migration program',
       "visa change",'sponsorship australia',"Skilled visa",
       "Visa","Visa law","Migration Australia","Immigrant",
       "Citizenship Australia","Permanent resident,","Visa subclass,",
       "visa 457","student visa Australia,","international students,",
       "partner visa","skilled migration","skilled occupation list,",
       "student migration","skilled immigration,","migration,",
       "department of immigration","work visa","refugee","migration policy","visa policy"]

#filename="keywordSearch"
count=0
loop=0
db_new=config.db_clean_setup(config.SERVER_ADDRESS)
found=False
for i in db_new.view('view/hasSuburbNoQuery'):#,reduce=True,group_level=1)
    if loop%500==0:
        print "Current loop: ",loop 
    doc=db_new[i.key]
    clean= TwitterSentiment.processTweet(doc['text'])
    for i in clean.split():
        for j in range(len(words)):
            if i in words[j]:
                doc['searchQuery']="migration"
                try:
                    db_new.save(doc)
                    count+=1
                    print "Added value"
                    found=True
                    break
                except:
                    print "Error DB"
                    continue
        if found==True:
            found=False
            break
    loop+=1
    