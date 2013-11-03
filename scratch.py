
import csv
import json
from Query import *
db = getCollection('practices',write=False)
totPatDic = {}
for res in db.find():
	print res
	try:
	 	# print res['metrics']['Total Patients']
		totPatDic[res['_id']] = res['metrics']['Total Patients']
	except:
		pass
print totPatDic
