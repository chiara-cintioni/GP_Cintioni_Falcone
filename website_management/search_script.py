import config


def search_org_name(org_name, collection, user_collection):
    if org_name == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Organism name': org_name
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_acc_num(acc_num, collection, user_collection):
    if acc_num == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Accession number': acc_num
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_length_from(length_from, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_length_to(length_to, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_length_from_to(length_from, length_to, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_length(length_from, length_to, collection, user_collection):
    if length_from == -1 and length_to == -1:
        return collection
    elif length_from != -1 and length_to == -1:
        return search_length_from(length_from, collection, user_collection)
    elif length_from == -1 and length_to != -1:
        return search_length_to(length_to, collection, user_collection)
    else:
        return search_length_from_to(length_from, length_to, collection, user_collection)


def search_benchmark(benchmark, collection, user_collection):
    if benchmark == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Benchmark ID': benchmark
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_num_decoup(num_decoup, collection, user_collection):
    if num_decoup == -1:
        return collection
    collection.aggregate([
        {
            '$match': {
                'Number of decoupled nucleotides': num_decoup
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_weak_from(weak_from, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_weak_to(weak_to, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_weak_from_to(weak_from, weak_to, collection, user_collection):
    collection.aggregate([
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
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_weak_bonds(weak_from, weak_to, collection, user_collection):
    if weak_from == -1 and weak_to == -1:
        return collection
    elif weak_from != -1 and weak_to == -1:
        return search_weak_from(weak_from, collection, user_collection)
    elif weak_from == -1 and weak_to != -1:
        return search_weak_to(weak_to, collection, user_collection)
    else:
        return search_weak_from_to(weak_from, weak_to, collection, user_collection)


def search_is_pseudo(is_pseudo, collection, user_collection):
    if is_pseudo == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Is Pseudoknotted': is_pseudo
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_pseudo_order(pseudo_order, collection, user_collection):
    if pseudo_order == -1:
        return collection
    collection.aggregate([
        {
            '$match': {
                'Pseudoknot order': pseudo_order
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_rna_type(rna_type, collection, user_collection):
    if rna_type == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Rna Type': rna_type
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_genus(genus, collection, user_collection):
    if genus == -1:
        return collection
    collection.aggregate([
        {
            '$match': {
                'Genus': genus
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_core(core, collection, user_collection):
    if core == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Core': core
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)

def search_core_plus(core_plus, collection, user_collection):
    if core_plus == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Core plus': core_plus
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_shape(shape, collection, user_collection):
    if shape == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Shape': shape
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_ena(collection, user_collection):
    collection.aggregate([
        {
            '$match': {
                'Taxonomy.ENA.Classified': 'Yes'
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_silva(collection, user_collection):
    collection.aggregate([
        {
            '$match': {
                'Taxonomy.SILVA.Classified': 'Yes'
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_ltp(collection, user_collection):
    collection.aggregate([
        {
            '$match': {
                'Taxonomy.LTP.Classified': 'Yes'
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_gtdb(collection, user_collection):
    collection.aggregate([
        {
            '$match': {
                'Taxonomy.GTDB.Classified': 'Yes'
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_ncbi(collection, user_collection):
    collection.aggregate([
        {
            '$match': {
                'Taxonomy.NCBI.Classified': 'Yes'
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_taxonomy(taxonomy, collection, user_collection):
    if taxonomy == '':
        return collection
    elif taxonomy == "SILVA":
        return search_silva(collection, user_collection)
    elif taxonomy == "ENA":
        return search_ena(collection, user_collection)
    elif taxonomy == "GTDB":
        return search_gtdb(collection, user_collection)
    elif taxonomy == "LTP":
        return search_ltp(collection, user_collection)
    else:
        return search_ncbi(collection, user_collection)


def get_string_ena(rank):
    string = "Taxonomy.ENA." + rank
    return string


def get_string_silva(rank):
    string = "Taxonomy.SILVA." + rank
    return string


def get_string_ltp(rank):
    string = "Taxonomy.LTP." + rank
    return string


def get_string_gtdb(rank):
    string = "Taxonomy.GTDB." + rank
    return string


def get_string_ncbi(rank):
    string = "Taxonomy.NCBI." + rank
    return string


def create_string_taxonomy(taxonomy, rank, value):
    string_array = []
    if taxonomy != '' and rank == '' and value == '':
        return ''
    if taxonomy == '' and rank == '' and value == '':
        return ''
    if taxonomy == "GTDB":
        if rank == 'superkingdom':
            rank = 'domain'
    if taxonomy == '' and rank != '' and value != '':
        string_array.append(get_string_silva(rank))
        string_array.append(get_string_ena(rank))
        string_array.append(get_string_ltp(rank))
        string_array.append(get_string_ncbi(rank))
        if rank == 'superkingdom':
            string_array.append(get_string_gtdb('domain'))
        else:
            string_array.append(get_string_gtdb(rank))
        return string_array
    elif rank != '' and value == '':
        return ''
    else:
        string = "Taxonomy." + taxonomy + "." + rank
        return string


def search_rank_all(string_array, value, collection, user_collection):
    config.DB.get_collection(user_collection).delete_many({})
    collection.aggregate([
        {
            '$match': {
                string_array[0]: value
            }
        }, {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    collection.aggregate([
        {
            '$match': {
                string_array[1]: value
            }
        },
        {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    collection.aggregate([
        {
            '$match': {
                string_array[2]: value
            }
        }, {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    collection.aggregate([
        {
            '$match': {
                string_array[3]: value
            }
        }, {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    collection.aggregate([
        {
            '$match': {
                string_array[4]: value
            }
        }, {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    return config.DB.get_collection(user_collection)


def search_rank(taxonomy, rank, value, collection, user_collection):
    string = create_string_taxonomy(taxonomy, rank, value)
    if string == '':
        return collection
    if type(string) == list:
        return search_rank_all(string, value, collection)
    else:
        collection.aggregate([
            {
                '$match': {
                    string: value
                }
            },
            {
                '$out': user_collection
            }
        ])
        return config.DB.get_collection(user_collection)


def get_file_with_one_taxonomy(filename, taxonomy, user_collection):
    collection = config.DB.get_collection("rna_sequences")
    string_taxonomy = 'Taxonomy.' + taxonomy + '.Classified'
    collection.aggregate([
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
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    return config.DB.get_collection(user_collection)


def search_db_name(db_name, collection, user_collection):
    if db_name == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Reference database': db_name
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)


def search_is_validated(is_validated, collection, user_collection):
    if is_validated == '':
        return collection
    collection.aggregate([
        {
            '$match': {
                'Is Validated': is_validated
            }
        },
        {
            '$out': user_collection
        }
    ])
    return config.DB.get_collection(user_collection)
