from pymongo import MongoClient

# Connecting to the MongoDB database.
CLIENT = MongoClient('localhost')
DB = CLIENT.PhyloRNAdb
COLLECTION = DB.rna_sequences
