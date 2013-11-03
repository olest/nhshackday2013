from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import re

#connection = Connection('146.185.159.107',27017)
def __connect__():
    connection = MongoClient('146.185.159.107', 27017)
    db = connection.prescription
    db.authenticate('nhshd','nhshd')
    return db

def getCollection(collName):
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



# res =  getAllAD()
# for r in res:
# 	print r


print sumAmounts()['result'][:5]
tmpListMetric = [{u'totalCost': 6.99, u'_id': u'C82651'}, {u'totalCost': 39.38, u'_id': u'C82642'}, {u'totalCost': 63.82, u'_id': u'C82639'}, {u'totalCost': 126.17, u'_id': u'C82624'}, {u'totalCost': 40.97, u'_id': u'C82610'}]
pushMetrics(id = tmpListMetric[0] )

# db = __connect__()
# print db.collection_names()
# pres = getCollection('prescriptons')
# print pres.find_one()

