from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = client.RIBOdb
#client = MongoClient('localhost')
#db = client.databaseRIBO

def search_org_name(org_name, collection):
    if org_name == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Organism name': org_name
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_acc_num(acc_num, collection):
    if acc_num == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Accession number': acc_num
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_length(length, collection):
    if length == -1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Length': length
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_benchmark(benchmark, collection):
    if benchmark == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Benchmark ID': benchmark
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_num_decoup(num_decoup, collection):
    if num_decoup == -1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Number of decoupled nucleotides': num_decoup
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_weak_bonds(wea_bon, collection):
    if wea_bon ==-1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Number of weak bonds': wea_bon
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_is_pseudo(is_pseudo, collection):
    if is_pseudo == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Is Pseudoknotted': is_pseudo
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_pseudo_order(pseudo_order, collection):
    if pseudo_order == -1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Pseudoknot order': pseudo_order
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_rna_type(rna_type, collection):
    if rna_type == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Rna Type': rna_type
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    res_c = res_col.find()
    for r in res_c:
        print(r['Organism name'])
    print(rna_type)
    return res_col

def search_genus(genus, collection):
    if genus == -1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Genus': genus
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_core(core, collection):
    if core == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Core': core
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_core_plus(core_plus, collection):
    if core_plus == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Core plus': core_plus
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_shape(shape, collection):
    if shape == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Shape': shape
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

