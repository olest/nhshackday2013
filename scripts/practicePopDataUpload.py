## Python script to upload practice level data to pymongo DB

import csv
import json
from Query import *
	
# with open("../data/pracPopData2.txt",'rb') as csvfile:
# 	reader = csv.reader(csvfile, delimiter='\t')
# 	out = {}
# 	for row in reader:
# 		out[row[0]] = {'Total Patients' : row[1]}

# with open('Patient.json','wb') as jsonout:
# 	json.dump(out,jsonout)
# pushToPrac(out)
# dic = {}
# for r in getAllAD():	

# # print len(dic.keys())
# pushToPrac(dic)
# testPrac(out)
totPatDic = {}
db = getCollection('practices',write=False)
for res in db.find():
	try:
	 	# print res['metrics']['Total Patients']
		totPatDic[res['_id']] = res['metrics']['Total Patients']
		# print res['_id'],res['metrics']['Total Patients']
	except:
		pass


# drugList = ['fluoxetine','citalopram','quetiapine','donepezil','metformin','sitagliptin','ferr']
drugList = ['fluoxetine']

dbwrite = getCollection('practices',write=True)
for drug in drugList:
	dic = {}
	res = getpres(drug)
	for r in res:
		pracID = r['PRACTICE']
		quan = r['QUANTITY']
		# dic[pracID] = {'Quanity of ' + r['BNF NAME'] : r['QUANTITY']}
		db = getCollection('practices',write=False)
		try: 
			# totPat = db.find_one({'_id':pracID})['metrics']['Total Patients']
			totPat = totPatDic[pracID]
			# dic[pracID] = 
			print {'Quanity of ' + r['BNF NAME']  + ' per patient' : float(quan)/float(totPat)}
			dbwrite.update({'_id':pracID},{'$set': {'metrics.'+'Quantity of ' + r['BNF NAME']  + ' per patient':float(quan)/float(totPat)} })

			# print dic[pracID]
		except:
			pass
	# print dic
	# pushToPrac(dic)




		

