function ss(doc){ 

function containsWord(text){
var i;
var keywords = ['immigration','migration','visa','#migration','#Australia','permanent migration program',
       "visa change",'sponsorship australia',"Skilled visa",
       "Visa","Visa law","Migration Australia","Immigrant",
       "Citizenship Australia","Permanent resident,","Visa subclass,",
       "visa 457","student visa Australia,","international students,",
       "partner visa","skilled migration","skilled occupation list,",
       "student migration","general skilled immigration,","migration,",
       "department of immigration","work visa","refugee","migration policy","visa policy"];
var words=text.split(" ");
var count=0
for (i = 0; i < words.length; i++) {
	if (keywords.includes(words[i]))
	{
 		count=count+1;
	}
}
return count
}
if(containsWord(doc.text)>0) {emit (doc._id,doc) }}