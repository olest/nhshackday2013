## Python script to upload practice level metrics to pymongo DB

import csv
import json
from Query import *
	
with open("data/metrics2.csv",'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	print 
	out = {}
	header = reader.next()
	print header

	# for row in reader:
	# 	out[row[0]] = {}
	# 	for i in range(len(row))[1:]:
	# 		out[row[0]].update({header[i] : row[i]}) 
	
pushToPrac(out)
with open('PatientMetrics.json','wb') as jsonout:
	json.dump(out,jsonout)