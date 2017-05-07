import config

#!/usr/bin/python
import json
import csv, sys, re
import config
from shapely.geometry import MultiPoint, Point

attributes = 'AurinData/age-attributes.csv'
nodes = 'AurinData/age-nodes.csv'
attributes2 = 'AurinData/edu-emp-attributes.csv'
suburbs = []
suburbDict={}

def tofloat(x):
    import numpy as no
    try:
        return float(x)
    except:
        return -1

#Get Age
with open(attributes, 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    reader.next()
    for row in reader:
        # remove all the float IDs as they represent the same area
        if re.match('^[0-9]+$', row[0]):
            suburbDict[row[0]]={}
            suburbDict[row[0]]['name'] = row[2]
            suburbDict[row[0]]['age60'] = tofloat(row[5])+tofloat(row[11])
            suburbDict[row[0]]['age50'] = tofloat(row[3])+tofloat(row[39])
            suburbDict[row[0]]['age40'] = tofloat(row[10])+tofloat(row[36])
            suburbDict[row[0]]['age30'] = tofloat(row[22])+tofloat(row[34])
            suburbDict[row[0]]['age20'] = tofloat(row[29])+tofloat(row[32])
            suburbDict[row[0]]['below20'] = tofloat(row[13])+tofloat(row[14])+tofloat(row[27])+tofloat(row[40])
            suburbs.append(row[0])

# get attributes from the first file
with open(attributes2, 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    reader.next()
    for row in reader:
        # remove all the float IDs as they represent the same area
        if re.match('^[0-9]+$', row[0]):
            #Check to see if we have Age data, otherwise skip
            try:
                suburbDict[row[0]]
                suburbDict[row[0]]['uni'] = tofloat(row[3])
                suburbDict[row[0]]['tafe'] = tofloat(row[4])
                suburbDict[row[0]]['highschool'] = tofloat(row[5])
                suburbDict[row[0]]['participation'] = tofloat(row[6])
                suburbDict[row[0]]['maleparticipation'] = tofloat(row[7])
                suburbDict[row[0]]['femaleparticipation'] = tofloat(row[8])
                suburbDict[row[0]]['employmentratio'] = tofloat(row[9])
                suburbDict[row[0]]['income'] = tofloat(row[11])
            except:
                continue

#Get Coordinates
totalCoordinates={}
with open(nodes, 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    for row in reader:
        coordinates = (tofloat(row[1]), tofloat(row[2]))
        try:
            totalCoordinates[row[0]].append(coordinates)
        except:
            totalCoordinates[row[0]]=[coordinates]

for i in totalCoordinates:
    try:
        suburbDict[i]['allCoordinates']=totalCoordinates[i]
    except:
        continue

polygons = {}
for i in suburbDict:
    poly = MultiPoint(suburbDict[i]['allCoordinates'].convex_hull)
    polygons[suburbDict[i]['name']] = poly

db=config.db_clean_setup(config.SERVER_ADDRESS)


# find the suburb for tweet location
for i in tweets:
	p = Point(i[0], i[1])
	for s in suburbs:
		if polygons[s].contains(p):
			print s
count=0
for i in db_new.view('view/hasGeo'):
    doc=db[i.key]
    point=Point(doc[i.key]['geo']['coordinates'][0],doc[i.key]['geo']['coordinates'][1])
    for s in polygons:
        print s
        if polygons[s].contains(point):
            print "Success"