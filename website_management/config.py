from pymongo import MongoClient

# Connecting to the MongoDB database.
CLIENT = MongoClient('localhost')
DB = CLIENT.RIBOdb
COLLECTION = DB.rna_sequences
