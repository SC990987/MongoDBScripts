# MongoDBScripts
MongoDB scripts for the CMS HGCAL ECON Team 

# Files
there are a few scripts in this repository
- jsonLoad.py: this has some tools for preproccesing the JSON files and an example of how to load the JSON Files into a nested list
- MongoFileUploader.py: this file helps the user upload JSON files to the database with the appropriate preprocessing. The user needs to supply the database and file directory
- MongoExample.py: this script has a function that can be used to print off the testing information for an individual test such as:
   - test name
   - how many chips passed the test
   - the total number of chips tested
   - the pass rate (#passed/total)
# Example data
the example data folder contains some old JSON Files from a previous round of ECONT testing 
