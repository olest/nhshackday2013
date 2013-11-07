from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import re
import config

#connection = Connection('146.185.159.107',27017)
def __connect__():
    connection = MongoClient(config.DB_SERVER,config.DB_PORT)
    db = connection.prescription
    db.authenticate(config.DB_USER,config.DB_PWD)
    return db

def __connectWrite__():
    connection = MongoClient(config.DB_SERVER, config.DB_PORT)
    db = connection.prescription
    db.authenticate(config.DB_USER_RW,config.DB_PWD_RW)
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
    elif collName=='prescriptions':
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
            print pracID
            r = db.update({'_id':pracID},{'$set': {'metrics.'+key:value} })
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

def getDerivedMetrics():
    db = getCollection('practices')
    metrics = set([])
    for practice in db.find({"metrics":{"$exists":1}}):
        metrics = metrics.union( set(practice["metrics"].keys()) )

    return metrics



def displayRules(name):
    Quanity = re.search('Quanity',name)
    perp = re.search('patient',name)
    totP = 'totPatient'==name
    if (Quanity and not perp) or totP or countMetrics(name) < 100 :
        return 0
    else:
        return 1


def editDisplay():
    db = getCollection('metrics',write=True)
    allMetrics = getDerivedMetrics()
    for metric in allMetrics:
        c = db.find({'name':metric}).count()
        d = displayRules(metric)
        if not c:
            db.insert({'name':metric,'display':d})
        else:
            db.update({'name':metric},{'$set':{'display':d}})
        print db.find_one({'name':metric},{'name':1,'display':1})

def countMetrics(name):
    db = getCollection('practices')
    return db.find({'metrics.'+name:{'$exists':1}}).count()








# drugOfInterest(['Quanity of Citalopram Hydrob_Tab 40mg','Quanity of Citalopram Hydrob_Tab 10mg','Quanity of Fluoxetine HCl_Cap 20mg','Total Patients',
#     'Deprivation score','% aged 65+ years','IDAOPI','% satisfied with phone access','Working status - Unemployed','Disability allowance claimants (per 1000)',
#     'All outpatient attendances (per 1000)','Diabetes: QOF prevalence (17+)','Psychoses: QOF prevalence (all ages)','Dementia: QOF prevalence (all ages)',
#     'Depression: QOF prevalence (18+)'])
# db = getCollection('metrics')
# db = getCollection('practices')
# res = db.find()
# for r in res:
#     print r






# res =  getAllAD()
# for r in res:
# 	print r


# print sumAmounts()['result'][:5]
# tmpListMetric = [{u'totalCost': 6.99, u'_id': u'C82651'}, {u'totalCost': 39.38, u'_id': u'C82642'}, {u'totalCost': 63.82, u'_id': u'C82639'}, {u'totalCost': 126.17, u'_id': u'C82624'}, {u'totalCost': 40.97, u'_id': u'C82610'}]
# pushMetrics(id = tmpListMetric[0] )

# db = __connect__()
# print db.collection_names()
# pres = getCollection('practices')
# for r in pres.find({}):
#     print r

