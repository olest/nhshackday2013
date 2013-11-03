from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import re
import csv
import geojson
import json

#connection = Connection('146.185.159.107',27017)
def __connect__():
    connection = MongoClient('146.185.159.107', 27017)
    db = connection.prescription
    db.authenticate('nhshd','nhshd')
    return db

def __connectWrite__():
    connection = MongoClient('146.185.159.107', 27017)
    db = connection.prescription
    db.authenticate('nhshd-rw','nhs-m0ng0')
    return db

def getCollection(collName,write=False):
    if write:
        db = __connectWrite__()
    else:
        db = __connect__()
    if collName=='system.indexes':
        posts = db.system.indexes
    elif collName=='practices':
        posts = db.practices
    elif collName=='chem_sub':
        posts = db.chem_sub
    elif collName=='practice_geo':
        posts = db.practice_geo
    elif collName=='prescriptons':
        posts = db.prescriptons
    elif collName=='system.users':
        posts = db.system.users
    else:
        raise Exception('Unknown database collection ' + collName)
    return posts



def getAllAD():
	p = getCollection('prescriptons')
	regx = re.compile("^0403030", re.IGNORECASE)
	res = p.find({'BNF CODE':regx})
	return res

def sumAmounts():
	## Function to aggregate 
	p = getCollection('prescriptons')
	# regx = re.compile("^0403030", re.IGNORECASE)
	regx = re.compile("^0403030E0", re.IGNORECASE)
	return p.aggregate( [{ '$match': {'BNF CODE':regx}  } , 
		{'$group': { '_id' : "$PRACTICE" ,'totalCost': {'$sum': "$ACT COST"} }}])	

def pushMetrics(id):
	## Function to take a list of dictonaries with id:practice and 
	# metricName and push to practice db
	db = getCollection('practices')
	print db.find({'_id':id})

def pushToPrac(dic):
    db = getCollection('practices',write=True)
    for pracID,pracDic in dic.iteritems():
        for key,value in pracDic.iteritems():
            r = db.update({'_id':pracID},{'$set': {'metrics':{key:value}} })

def testPrac(dic):
    db = getCollection('practices',write=False)
    for pracID,pracDic in dic.iteritems():
        res = db.find({'_id':pracID})
        for r in res:
            print r


def main():
    cl  = getCollection('practices',write=False)
    print '{ "type": "FeatureCollection",','\n'; 
    print '"features": [','\n'
    for p in cl.find({ 'loc' : { '$exists' : True} }) :
        print '{ "type": "Feature",'
        print '"properties" : { '
        print '"Name" : "',p['name'],'"',
        print '"Post code" : "',p['post'],'"',
        print '"Town" : "',p['town'],'"',
        print'}\n'
        print '"geometry": { "type": "Point", "coordinates": [',p['loc']['coordinates'][0],',',p['loc']['coordinates'][1],'] }\n'; 
        print '}',"\n"
    print "]\n"
    print "}"

    #with open('data.geojson', 'w') as outfile:
    #with open("geo.practice.csv", "w") as file:
        #csv_file = csv.writer(file)
            #print p['loc']['coordinates'][0]
            #f.write(['loc']['coordinates'][0],
            #                  p['loc']['coordinates'][1]  
            #                 ])
            #print pt;
            #json.dump(p['loc'],outfile)
            #csv_file.writerow([p['name'].lstrip(),
            #                   p['town'].lstrip(),
            #                   p['post'].lstrip(),
            #                   p['loc']['coordinates'][0],
            #                   p['loc']['coordinates'][1]
            #                  ]);

    #f.close()
    

    #practiceID = 'D81025'
    #cl  = getCollection('prescriptons',write=False)
    #print "Number of prescriptions for practice ",practiceID," : \n";
    #print cl.find({"PRACTICE": practiceID}).count()
    #for pr in cl.find({"PRACTICE": practiceID}).sort("ACT_COST",DESCENDING) :
    #    print pr

if __name__ == "__main__":
    main()


# res =  getAllAD()
# for r in res:
# 	print r


# print sumAmounts()['result'][:5]
# tmpListMetric = [{u'totalCost': 6.99, u'_id': u'C82651'}, {u'totalCost': 39.38, u'_id': u'C82642'}, {u'totalCost': 63.82, u'_id': u'C82639'}, {u'totalCost': 126.17, u'_id': u'C82624'}, {u'totalCost': 40.97, u'_id': u'C82610'}]
# pushMetrics(id = tmpListMetric[0] )

# db = __connect__()
# print db.collection_names()
# pres = getCollection('practices')
# print pres.find_one()

