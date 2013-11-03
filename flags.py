## edit flags

import csv
import json
from Query import *

db = getCollection('metrics')
res = db.find_one({'name': 'Total Patients'})
for r in res:
	print r