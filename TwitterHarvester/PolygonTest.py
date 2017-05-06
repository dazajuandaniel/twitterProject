#!/usr/bin/python
import csv, sys
from shapely.geometry import MultiPoint, Point
import config

suburbs = []
polyCors = {}

#DB Connection
db=config.db_clean_setup(config.SERVER_ADDRESS)

with open('data/age-attributes.csv', 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    reader.next()
    for row in reader:
        suburbs.append(row[0])

with open('data/age-nodes.csv', 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    reader.next()
    for code in suburbs:
        for row in reader:
            points = []
            if code == row[0]:
                coordinates = (row[1], row[2])
                points.append(coordinates)
        polyCors[code] = points

polygons = {}
for n in suburbs:
	poly = MultiPoint(polyCors[n]).convex_hull
	polygons[n] = poly

for i in db.view('view/hasGeo'):
    lat=db[i.id]['geo']['coordinates'][1]
    lon=db[i.id]['geo']['coordinates'][0]
    point=Point(lat,lon)
    for suburb in suburbs:
        if polygons[suburb].contains(point):
            print suburb
    print "Not Found", lat," ",lon