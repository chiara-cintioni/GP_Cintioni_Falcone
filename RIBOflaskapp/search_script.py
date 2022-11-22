from pymongo import MongoClient

#client = MongoClient('mongodb://localhost:27017', 27017)
client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
#client = MongoClient('localhost')
db = client.RIBOdb
#db = client.RIBO_flask_db


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


def search_length(length_from, length_to, collection):
    if length_from == -1 and length_to == -1:
        return collection
    elif length_from != -1 and length_to == -1:
        return search_length_from(length_from, collection)
    elif length_from == -1 and length_to != -1:
        return search_length_to(length_to, collection)
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


def search_weak_bonds(weak_from, weak_to, collection):
    if weak_from == -1 and weak_to == -1:
        return collection
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


def search_ENA(collection):
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


def search_SILVA(collection):
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


def search_LTP(collection):
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


def search_GTDB(collection):
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


def search_NCBI(collection):
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
        return search_SILVA(collection)
    elif taxonomy == "ENA":
        return search_ENA(collection)
    elif taxonomy == "GTDB":
        return search_GTDB(collection)
    elif taxonomy == "LTP":
        return search_LTP(collection)
    else:
        return search_NCBI(collection)


def get_string_ENA(rank):
    string = "Taxonomy.ENA."+rank
    return string


def get_string_SILVA(rank):
    string = "Taxonomy.SILVA."+rank
    return string


def get_string_LTP(rank):
    string = "Taxonomy.LTP."+rank
    return string


def get_string_GTDB(rank):
    string = "Taxonomy.GTDB."+rank
    return string


def get_string_NCBI(rank):
    string = "Taxonomy.NCBI."+rank
    return string


def create_string_taxonomy(taxonomy, rank, value):
    print("Sono in create string taxonomy iniziale")
    string_array = []
    if taxonomy != '' and rank == '' and value == '':
        return ''
    if taxonomy == '' and rank == '' and value == '':
        return ''
    if taxonomy == "GTDB":
        if rank == 'superkingdom':
            rank = 'domain'
    if taxonomy == '' and rank != '' and value != '':
        string_array.append(get_string_SILVA(rank))
        string_array.append(get_string_ENA(rank))
        string_array.append(get_string_LTP(rank))
        string_array.append(get_string_NCBI(rank))
        if rank == 'superkingdom':
            string_array.append(get_string_GTDB('domain'))
        else:
            string_array.append(get_string_GTDB(rank))
        print("Sto nel caso senza tassonomia. L'array è:")
        for i in string_array:
            print(i)
        return string_array
    elif rank != '' and value == '':
        return ''
    else:
        string = "Taxonomy."+taxonomy+"."+rank
        return string


def search_rank_all(string_array, value, collection):
    print(string_array, value)
    db.get_collection("temp").delete_many({})
    result = collection.aggregate([
        {
            '$match': {
                string_array[0]: value
            }
        }, {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    result = collection.aggregate([
        {
            '$match': {
                string_array[1]: value
            }
        },
        {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    print("ci stava qualcosa")
    result = collection.aggregate([
        {
            '$match': {
                string_array[2]: value
            }
        }, {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    result = collection.aggregate([
        {
            '$match': {
                string_array[3]: value
            }
        }, {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    result = collection.aggregate([
        {
            '$match': {
                string_array[4]: value
            }
        }, {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    res_col = db.temp

    return res_col

def search_rank(taxonomy, rank, value, collection):
    string = create_string_taxonomy(taxonomy, rank, value)
    if string == '':
        return collection
    if type(string) == list:
        return search_rank_all(string, value, collection)
    else:
        result = collection.aggregate([
            {
                '$match': {
                    string: value
                }
            },
            {
                '$out': 'temp'
            }
        ])
        res_col = db.temp
        return res_col


def get_file_with_one_taxonomy(filename, taxonomy):
    collection = db.get_collection("rna_sequences")
    string_taxonomy = 'Taxonomy.'+taxonomy+'.Classified'
    result = collection.aggregate([
            {
                '$match': {
                    'Benchmark ID': filename
                }
            }, {
            '$unwind': {
                'path': '$Taxonomy',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                '$or': [
                    {
                        string_taxonomy: 'No'
                    }, {
                        string_taxonomy: 'Yes'
                    }
                ]
            },

        }, {
            '$merge': {
                'into': 'temp',
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    res_col = db.temp
    return res_col


def search_db_name (db_name,collection):
    if db_name == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Reference database': db_name
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col

def search_is_validated (is_validated, collection):
    if is_validated == '':
        return collection
    result = collection.aggregate([
        {
            '$match': {
                'Is Validated': is_validated
            }
        },
        {
            '$out': 'temp'
        }
    ])
    res_col = db.temp
    return res_col