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
def checkMigration(text):
    for word in text.split():
        for keyword in range(len(WORDS)):
            if word in WORDS[keyword] and len(word)==len(WORDS[keyword]):
                return "migration"
    return "Other Topic"