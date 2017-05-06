#!/usr/bin/python
import json
import csv, sys, re
from shapely.geometry import MultiPoint, Point

attributes = 'age-attributes.csv'
nodes = 'age-nodes.csv'
suburbs = []
name = {}
age60 = {}
age50 = {}
age40 = {}
age30 = {}
age20 = {}
below20 = {}
allCoordinates = {}

# get attributes from the first file
with open(attributes, 'rb') as f:
	reader = csv.reader(f, delimiter = ',')
	reader.next()
	for row in reader:
		# remove all the float IDs as they represent the same area
		if re.match('^[0-9]+$', row[0]):
			suburbs.append(row[0])
			name[row[0]] = row[2]
			age60[row[0]] = float(row[5])+float(row[11])
			age50[row[0]] = float(row[3])+float(row[39])
			age40[row[0]] = float(row[10])+float(row[36])
			age30[row[0]] = float(row[22])+float(row[34])
			age20[row[0]] = float(row[29])+float(row[32])
			below20[row[0]] = float(row[13])+float(row[14]+float(row[27])+float(row[40]))

# get coordinates from the second file
for code in suburbs:
	with open(nodes, 'rb') as f:
		reader = csv.reader(f, delimiter = ',')
		reader.next()
		points = []
		for row in reader:
			if code == row[0]:
				coordinates = (float(row[1]), float(row[2]))
				points.append(coordinates)
		allCoordinates[code] = points

# create polygons for each suburb
polygons = {}
for n in suburbs:
	poly = MultiPoint(allCoordinates[n]).convex_hull
	polygons[n] = poly

with open('smallTwitter.json') as tw:
	tweets = []
	for line in tw:
		if line == '[\n':
			continue
		if line == ']\n':
			break
		content = json.loads(line.replace(",\n", "\n"))
		jsonDict = content['json']
		coordinates = jsonDict['coordinates']
		point = coordinates['coordinates']
		tweets.append(point)
tw.close()

# find the suburb for tweet location
for i in tweets:
	p = Point(i[0], i[1])
	for s in suburbs:
		if polygons[s].contains(p):
			print s