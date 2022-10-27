import os
import pymongo
import gridfs
from tkinter import *
from tkinter import filedialog




myclient=pymongo.MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test',27017)
db = myclient['RIBOdb']
collection = db['rna_sequences']
fs = gridfs.GridFS(db)

def choose_path(format):
    win = Tk()
    win.attributes('-topmost', True)
    win.withdraw()
    path = filedialog.askdirectory(title="Choose a directory for your "+format+" files")
    return path


def download_db_nh_files(ref_ids):
    dir_path = choose_path("db_nh")
    for single_id in ref_ids:
        if single_id != '':
            name = single_id + "_nH.db"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


def download_bpseq_nh_files(ref_ids):
    dir_path = choose_path("bpseq_nh")
    for single_id in ref_ids:
        if single_id != '':
            name = single_id + "_nH.bpseq"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


def download_ct_nh_files(ref_ids):
    dir_path = choose_path("ct_nh")
    for single_id in ref_ids:
        if single_id != '':
            #modificare qui per prendere i ct senza header!!!
            name = single_id + ".ct"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


def download_db_files(ref_ids):
    dir_path = choose_path("db")
    for single_id in ref_ids:
        if single_id != '':
            name = single_id + ".db"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


def download_bpseq_files(ref_ids):
    dir_path = choose_path("bpseq")
    for single_id in ref_ids:
        if single_id != '':
            name = single_id + ".bpseq"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


def download_ct_files(ref_ids):
    dir_path = choose_path("ct")
    for single_id in ref_ids:
        if single_id != '':
            name = single_id + ".ct"
            data = db.fs.files.find_one({'filename': name})
            my_id = data['_id']
            output_data = fs.get(my_id).read()
            download_loc = dir_path + "/" + name
            output = open(download_loc, "wb")
            output.write(output_data)
            output.close()
            print("Download completed")


