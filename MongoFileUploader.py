#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from pymongo import MongoClient, InsertOne
import numpy as np
import glob
import json

## Grab JSON Files
idir = "/Users/alexcampbell/Documents/Research/Fermilab/ECONT_Retest/March2024" ##  Change to your directory
fnames = list(np.sort(glob.glob(f"{idir}/report*.json")))

## Connect to a local Database
client = pymongo.MongoClient("mongodb://127.0.0.1:27017") # Connect to local database
session = client.start_session()

mydatabase = client['jsonDB'] # create new database
mycol = mydatabase['ECONT']

def selector(input):
    if input == 'passed':
        return 1
    elif input == 'failed':
        return 0
    ## This is for a test that was skipped
    else:
        return -1

def stringReplace(word):
    if "[" in word:
        word = word.replace("[","_")
    if ".." in word:
        word = word.replace("..","_")
    if "/" in word:
        word = word.replace("/","_")
    if "]" in word:
        word = word.replace("]", "")
    return word

def jsonFileUploader(fname):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    ## preprocess the JSON file
    dict = {
            "summary": {'passed': data['summary']['passed'], 'total':data['summary']['total'], 'collected':data['summary']['collected']},
            "individual_test_outcomes": {
                f"{stringReplace(test['nodeid'].split('::')[1])}": selector(test['outcome']) for test in data['tests']
            },
            "tests":{
                f"{stringReplace(test['nodeid'].split('::')[1])}": {
                    "metadata": test['metadata'] if 'metadata' in test else None,
                    "failure_information":{
                        "failure_mode": test['call']['traceback'][0]['message'] if test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                        "failure_cause": test['call']['crash']['message'],
                        "failure_code_line": test["call"]["crash"]["lineno"],
                    } if 'failed' in test['outcome'] else None,
                } for test in data['tests']
            },
            "identifier": data['chip_number'],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            }
    ## Insert File into the DB 
    x = mycol.insert_one(dict) # Write in DB

## upload all the JSON files in the database
for i, (fname) in enumerate(fnames):
    try:
        jsonFileUploader(fname)
    except Exception as e:
        print(e, fname, i)

