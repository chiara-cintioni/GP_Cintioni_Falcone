import json
import os
import pymongo


myclient = pymongo.MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = myclient['RIBOdb']
collection = db['rna_sequences']


def insert_many_to_mongo(dir_path):
    for file_to_read in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_to_read)
        if os.path.isfile(file_path):
            with open(file_path, 'r+') as file:
                file_data = json.load(file)
                if isinstance(file_data, list):
                    collection.insert_many(file_data)
                else:
                    collection.insert_one(file_data)
    print("The json files have been inserted to mongo db. \n")


def update_one_field():
    acc_number = input("Insert the accession number of the rna sequence you want to modify: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        update_one_field()
    field = input(("Insert the field you want to change: "))
    new_input = input("Insert the new value of the field: ")
    collection.find_one_and_update({"Accession number": acc_number}, {"$set": {field: new_input}})
    if new_input == old_document.get(field):
        print("Sorry, we couldn't update the value.")
    else:
        print("The value was changed successfully.")
        print(collection.find_one({"Accession number": acc_number}))


def delete_one():
    acc_number = input("Insert the accession number of the rna sequence you want to delete: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        delete_one()
    print("Are you sure you want to delete this document? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        collection.find_one_and_delete({"Accession number": acc_number})
        print("The document has been deleted. \n")
    else:
        print("Operation Aborted. \n")


def delete_all():
    col_name = input("Insert the name of the collection of the documents you want to delete: ")
    print("Are you sure you want to delete all documents of this collection? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        db.get_collection(col_name).delete_many({})
        print("All documents have been deleted. \n")
    else:
        print("Operation Aborted. \n")