from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import re

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
    elif collName=='metrics':
        posts = db.metrics
    else:
        raise Exception('Unknown database collection ' + collName)
    return posts



def getAllAD():
	p = getCollection('prescriptons')
	regx = re.compile("^0403030", re.IGNORECASE)
	res = p.find({'BNF CODE':regx})
	return res


def getpres(presname=""):
    p = getCollection('prescriptons')
    regx = re.compile(presname, re.IGNORECASE)
    res = p.find({'BNF NAME':regx})
    return res




def sumAmounts():
	## Function to aggregate 
	p = getCollection('prescriptons')
	# regx = re.compile("^0403030", re.IGNORECASE)
	regx = re.compile("^0403030E0", re.IGNORECASE)
	return p.aggregate( [{ '$match': {'BNF CODE':regx}  } , 
		{'$group': { '_id' : "$PRACTICE" ,'totalCost': {'$sum': "$ACT COST"} }}])	

# def pushMetrics(id):

# 	db = getCollection('practices')
# 	print db.find({'_id':id})

def pushToPrac(dic):
        ## Function to take a list of dictonaries with id:practice and 
    # metricName and push to practice db
    db = getCollection('practices',write=True)
    print 'Start Upload'
    for pracID,pracDic in dic.iteritems():
        for key,value in pracDic.iteritems():
            r = db.update({'_id':pracID},{'$set': {'metrics.'+key:float(value)} })
    print "Finish"

def testPrac(dic):
    db = getCollection('practices',write=False)
    for pracID,pracDic in dic.iteritems():
        res = db.find({'_id':pracID})
        for r in res:
            print r



def drugOfInterest(listDrug=""):
    ## Takes a list of drugs and uploads to db
    db = getCollection('metrics',write=True)
    db.insert({'MetricList':listDrug})





drugOfInterest(['Quanity of Citalopram Hydrob_Tab 40mg','Quanity of Citalopram Hydrob_Tab 10mg','Quanity of Fluoxetine HCl_Cap 20mg','Total Patients',
    'Deprivation score','% aged 65+ years','IDAOPI','% satisfied with phone access','Working status - Unemployed','Disability allowance claimants (per 1000)',
    'All outpatient attendances (per 1000)','Diabetes: QOF prevalence (17+)','Psychoses: QOF prevalence (all ages)','Dementia: QOF prevalence (all ages)',
    'Depression: QOF prevalence (18+)'])
db = getCollection('metrics')
print db.find_one()






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

