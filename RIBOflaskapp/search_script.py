from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db = client.RIBOdb
# client = MongoClient('localhost')
# db = client.databaseRIBO


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


def search_any_length(length, collection):
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


def search_length_from (length_from, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Length_match': {
                    '$gte': [
                        '$Length', length_from
                    ]
                }
            }
        }, {
            '$match': {
                'Length_match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_length_to(length_to, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Length_match': {
                    '$lte': [
                        '$Length', length_to
                    ]
                }
            }
        }, {
            '$match': {
                'Length_match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_length_from_to(length_from, length_to, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Length_match': {
                    '$gte': [
                        '$Length', length_from
                    ]
                }
            }
        }, {
            '$match': {
                'Length_match': True
            }
        }, {
            '$addFields': {
                'Length_match': {
                    '$lte': [
                        '$Length', length_to
                    ]
                }
            }
        }, {
            '$match': {
                'Length_match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_length(length_from, length_to, any_length, collection):
    if length_from == -1 and length_to == -1 and any_length == -1:
        return collection
    elif length_from == -1 and length_to == -1 and any_length != -1:
        return search_any_length(any_length, collection)
    elif length_from != -1 and length_to == -1:
        return search_length_from(length_from,collection)
    elif length_from == -1 and length_to != -1:
        return search_length_to(length_to,collection)
    else:
        return search_length_from_to(length_from, length_to, collection)


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


def search_any_weak(weak, collection):
    if weak == -1:
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Number of weak bonds': weak
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_weak_from(weak_from, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Number of weak bonds match': {
                    '$gte': [
                        '$Number of weak bonds', weak_from
                    ]
                }
            }
        }, {
            '$match': {
                'Number of weak bonds match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_weak_to(weak_to, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Number of weak bonds match': {
                    '$lte': [
                        '$Number of weak bonds', weak_to
                    ]
                }
            }
        }, {
            '$match': {
                'Number of weak bonds match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_weak_from_to(weak_from, weak_to, collection):
    result = collection.aggregate([
        {
            '$addFields': {
                'Number of weak bonds match': {
                    '$gte': [
                        '$Number of weak bonds', weak_from
                    ]
                }
            }
        }, {
            '$match': {
                'Number of weak bonds match': True
            }
        }, {
            '$addFields': {
                'Number of weak bonds match': {
                    '$lte': [
                        '$Number of weak bonds', weak_to
                    ]
                }
            }
        }, {
            '$match': {
                'Number of weak bonds match': True
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_weak_bonds(weak_from, weak_to, any_weak, collection):
    if weak_from == -1 and weak_to == -1 and any_weak == -1:
        return collection
    elif weak_from == -1 and weak_to == -1 and any_weak != -1:
        return search_any_weak(any_weak, collection)
    elif weak_from != -1 and weak_to == -1:
        return search_weak_from(weak_from, collection)
    elif weak_from == -1 and weak_to != -1:
        return search_weak_to(weak_to, collection)
    else:
        return search_weak_from_to(weak_from, weak_to, collection)


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


def search_taxonomy_ENA(collection):
    result = collection.aggregate([
        {
            '$match': {
                'Taxonomy.ENA.Classified': 'Yes'
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_taxonomy_SILVA( collection):
    result = collection.aggregate([
        {
            '$match': {
                'Taxonomy.SILVA.Classified': 'Yes'
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_taxonomy_LTP(collection):
    result = collection.aggregate([
        {
            '$match': {
                'Taxonomy.LTP.Classified': 'Yes'
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_taxonomy_GTDB(collection):
    result = collection.aggregate([
        {
            '$match': {
                'Taxonomy.GTDB.Classified': 'Yes'
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_taxonomy_NCBI(collection):
    result = collection.aggregate([
        {
            '$match': {
                'Taxonomy.NCBI.Classified': 'Yes'
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col


def search_taxonomy(taxonomy, collection):
    if taxonomy == '':
        return collection
    elif taxonomy == "SILVA":
        return search_taxonomy_SILVA(collection)
    elif taxonomy == "ENA":
        return search_taxonomy_ENA(collection)
    elif taxonomy == "GTDB":
        return search_taxonomy_GTDB(collection)
    elif taxonomy == "LTP":
        return search_taxonomy_LTP(collection)
    else:
        return search_taxonomy_NCBI(collection)


def search_domain(domain, collection):
    if domain == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Domain': domain
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col