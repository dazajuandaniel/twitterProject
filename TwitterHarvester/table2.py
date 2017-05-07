#!/usr/bin/python
import json
import csv, sys, re
from shapely.geometry import MultiPoint, Point

attributes = 'AurinData/edu-emp-attributes.csv'
nodes = 'AurinData/edu-emp-nodes.csv'
suburbs = []
name = {}
uni = {}
tafe = {}
high = {}
participation = {}
male_part = {}
female_part = {}
employ_ratio = {}
income = {}
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
			uni[row[0]] = float(row[3])
			tafe[row[0]] = float(row[4])
			high[row[0]] = float(row[5])
			participation[row[0]] = float(row[6])
			male_part[row[0]] = float(row[7])
			female_part[row[0]] = float(row[8])
			employ_ratio[row[0]] = float(row[9])
			income[row[0]] = float(row[11])

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
