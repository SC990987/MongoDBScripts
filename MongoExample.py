#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from pymongo import MongoClient
from MongoDBtools import testSummaryInformation

client = pymongo.MongoClient("mongodb://127.0.0.1:27017") # Connect to local database
session = client.start_session()

mydatabase = client['jsonDB'] # create new database
mycol = mydatabase['ECONT']

testNames = ['test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_',
 'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_',
 'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_0',
 'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_',
 'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_1',
 'test_bist',
 'test_common_mode_erx_route',
 'test_errBit_129-128',
 'test_errBit_129-16',
 'test_fc_lock',
 'test_rw_allregisters_0',
 'test_rw_allregisters_255',
 'test_hard_reset_i2c_allregisters',
 'test_soft_reset_i2c_allregisters',
 'test_wrong_reg_address',
 'test_alladdresses_0',
 'test_alladdresses_1',
 'test_alladdresses_2',
 'test_alladdresses_3',
 'test_alladdresses_4',
 'test_alladdresses_5',
 'test_alladdresses_6',
 'test_alladdresses_7',
 'test_alladdresses_8',
 'test_alladdresses_9',
 'test_alladdresses_10',
 'test_alladdresses_11',
 'test_alladdresses_12',
 'test_alladdresses_13',
 'test_alladdresses_14',
 'test_alladdresses_15',
 'test_wrong_i2c_address',
 'test_hold_hard_reset',
 'test_hold_soft_reset',
 'test_chip_sync',
 'test_input_aligner_shift_shift0-1-2',
 'test_input_aligner_shift_shift0-2-2',
 'test_ePortRXPRBS',
 'test_eTX_delayscan',
 'test_eTx_PRBS7',
 'test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0',
 'test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01',
 'test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012',
 'test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123',
 'test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234',
 'test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random.csv-fc_sequence6-ZS_37',
 'test_pllautolock',
 'test_pll_capbank_width',
 'test_pll_lock',
 'test_currentdraw_1p2V',
 'test_serializer']

def testSummaryInformation(testname):
    result = list(mycol.aggregate([
        {
            "$group": {
                '_id': f'{testname}',
                'pass': {"$sum":f"$individual_test_outcomes.{testname}"},
                'count': {"$sum":1},
            },
            
        },
        {
          "$addFields":{
                'passRate': {"$divide":["$pass","$count"]},
            },  
        }
    ]))
    return result

for name in testNames:
    print(list(testSummaryInformation(name)))

