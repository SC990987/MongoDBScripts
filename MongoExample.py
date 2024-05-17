#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from pymongo import MongoClient
from MongoDBtools import testSummaryInformation
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use([hep.style.ROOT, hep.style.firamath])

client = pymongo.MongoClient("mongodb://127.0.0.1:27017") # Connect to local database
session = client.start_session()

mydatabase = client['jsonDB'] # create new database
mycol = mydatabase['ECONT']

data = pd.DataFrame(list(mycol.aggregate([
            {
                "$project":{'testResults':{"$objectToArray":"$individual_test_outcomes"}}
            },
            {
                "$unwind":"$testResults"
            },    
            {
                "$group": {
                '_id': "$testResults.k",
                'pass': {"$sum":"$testResults.v"},
                'count': {"$sum":1},},
            },
            {
                "$sort":{'_id':1},
            },
            {
              "$addFields":{
                    'passRate': {"$divide":["$pass","$count"]},
            },  
        }
    ])))

label = data[data['passRate']>-1.0]['_id']
vals = data[data['passRate']>-1.0]['passRate']
plt.bar(label,vals)
plt.xticks(rotation=90, fontsize = 12)
plt.title("ECON Testing Pass Rates")
plt.ylabel("Pass Rates")
plt.savefig(f'./example-plot.png', dpi=300, facecolor = "w")

