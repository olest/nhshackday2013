## File for uploading metrics to practice DB from json file
import json
from Query import pushToPrac
import sys

f =  sys.argv[1]


def checkDic(dic):
	## Function to check correct form of dic
	return True

with open(f,'rb') as jsonfile:
	dic = json.load(jsonfile)
	if checkDic(dic): 
		pushToPrac(dic)