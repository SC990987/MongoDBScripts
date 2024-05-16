#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json
import numpy as np

def jsonload(fname):
    with open(fname) as jsonfile:
        try:
            return json.load(jsonfile)
        except Exception:
            print(fname)

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

def jsonParser(fname):
    with open(fname) as jsonfile:
        try:
            data = json.load(jsonfile)
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
            return dict
        except Exception:
            print(fname)


#####EXAMPLE USE#####
##import glob
##import jsonLoad
#####define input directory and import files
##idir = "/Users/alexcampbell/Documents/Research/Fermilab/ECONT_Retest/March2024"
##fnames = list(np.sort(glob.glob(f"{idir}/report*.json")))
#####load in the JSON Files. This will create a list of dictionaries. Each entry is the information from one JSON File
##ECONT = [jsonParser(fname) for fname in fnames if jsonParser(fname) is not None]

