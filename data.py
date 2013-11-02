from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import re

db = None

def __init__():
  if not db:
    connection = MongoClient('146.185.159.107', 27017)
    db = connection.prescription
    db.authenticate('nhshd','nhshd')

def getPractices():
  db.
  









