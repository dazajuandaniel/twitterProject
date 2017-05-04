#!/usr/bin/python
import csv, sys
from shapely.geometry import MultiPoint, Point

suburbs = []
polyCors = {}

with open('age-attributes.csv', 'rb') as f:
	reader = csv.reader(f, delimiter = ',')
	reader.next()
	for row in reader:
		suburbs.append(row[0])

with open('age-nodes.csv', 'rb') as f:
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

# check whether point p is inside the first suburb or not
p = Point(1.0, -2.1)
print polygons['0'].contains(p)

# search for the suburb which contains point p
for s in suburbs:
	if polygons[s].contains(p):
		print s
		break
		