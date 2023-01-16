import os
import pymongo
import gridfs

myclient = pymongo.MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = myclient['RIBOdb']
collection = db['rna_sequences']

"""
name = "CRW_5S_A_C_22.db"
name_nh = "CRW_5S_A_C_22"
file_location = "files/benchmark_db_files/CRW_5S_A_C_22.db"
file_data = open(file_location, "rb")
data = file_data.read()
fs = gridfs.GridFS(db)
fs.put(data, filename=name, _id=name_nh)
print("Upload completed")


data = db.fs.files.find_one({'filename': name})
my_id = data['_id']
output_data = fs.get(my_id).read()
download_loc = "C:\\Users\\Denise\\Desktop\\file\\" + name
output = open(download_loc, "wb")
output.write(output_data)
output.close()
print("Download completed")
"""


def insert_db_file():
    dir_path = input("Insert the path of the directory containing the db files: ")
    for file_to_read in os.listdir(dir_path):
            file_location = dir_path + "/" + file_to_read
            if os.path.isfile(file_location):
                file_data = open(file_location, "rb")
                data = file_data.read()
                fs = gridfs.GridFS(db)
                fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def insert_db_file_nh():
    dir_path = input("Insert the path of the directory containing the db files with no header: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def insert_bpseq_file_nh():
    dir_path = input("Insert the path of the directory containing the bpseq files with no header: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def insert_bpseq_file():
    dir_path = input("Insert the path of the directory containing the bpseq files: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def insert_ct_file_nh():
    dir_path = input("Insert the path of the directory containing the ct files with no header: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def insert_ct_file():
    dir_path = input("Insert the path of the directory containing the ct files: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


def files_menu():
    print("Choose what kind of file you want to insert into the db.")
    print("1. Files with .db extension.")
    print("2. Files with .db extension but no header.")
    print("3. Files with .ct extension.")
    print("4. Files with .ct extension but no header.")
    print("5. Files with .bpseq extension.")
    print("6. Files with .bpseq extension but no header.")
    print("0. Exit.")
    answer = input("Insert your choice: ")
    if not answer.isnumeric():
        print("You can only insert a number.")
        files_menu()
    if answer == 0:
        return
    elif int(answer) == 1:
        insert_db_file()
        files_menu()
    elif int(answer) == 2:
        insert_db_file_nh()
        files_menu()
    elif int(answer) == 3:
        insert_ct_file()
        files_menu()
    elif int(answer) == 4:
        insert_ct_file_nh()
        files_menu()
    elif int(answer) == 5:
        insert_bpseq_file()
        files_menu()
    elif int(answer) == 6:
        insert_bpseq_file_nh()
        files_menu()


