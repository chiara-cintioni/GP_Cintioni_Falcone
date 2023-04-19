from pymongo import MongoClient

# Connecting to the MongoDB database.
# CLIENT = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
CLIENT = MongoClient('localhost')
DB = CLIENT.RIBOdb
COLLECTION = DB.rna_sequences
