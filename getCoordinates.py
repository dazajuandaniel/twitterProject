#!/usr/bin/python
import json
import csv, sys
from shapely.geometry import MultiPoint, Point

suburbs = []
# key = suburb code, value = [(x,y)]
polyCors = {}	

with open('age-attributes.csv', 'rb') as f:
	reader = csv.reader(f, delimiter = ',')
	reader.next()
	for row in reader:
		suburbs.append(row[0])

for code in suburbs:
	with open('age-nodes.csv', 'rb') as f:
		reader = csv.reader(f, delimiter = ',')
		reader.next()
		points = []
		for row in reader:
			if code == row[0]:
				coordinates = (row[1], row[2])
				points.append(coordinates)
		polyCors[code] = points
		print code, polyCors[code]