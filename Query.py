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

db= __connect__()
print db.collection_names()
pres = getCollection('prescriptons')
print pres.find_one()

#print db.collection_names()
def getAllAD():
	p = getCollection('prescriptons')
	regx = re.compile("^0403030", re.IGNORECASE)
	res = p.find({'BNF CODE':regx})
	return res

def sumAmounts():
	p = getCollection('prescriptons')
	regx = re.compile("^0403030", re.IGNORECASE)
	print p.aggregate( [{ '$match': {'BNF CODE':regx}  } , {'$group': { '_id' : "$PRACTICE" },'$total': {'$sum': "$ACT COST"} }])



getAllAD()
sumAmounts()

