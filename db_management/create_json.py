from create_rna_object import RnaObject
import os
import pandas as pd

rank_file = open("files/taxonomy/TaxaName_TaxaRank.txt", "r")
dataframe = pd.read_table(rank_file)
rank_file.close()


def read_files():
    dir_path = input("Insert the path of the directory that contains ONLY the txt files: ")
    for file_to_read in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_to_read)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                if f.name.endswith(".txt"):
                    output_path = "files/json_files"
                    output = file_to_read.replace(".txt", ".json")
                    print("Creating json of: ", output)
                    output = open(os.path.join(output_path, output), "w")
                    create_file_json(f, output)
    print("The creation of the json files to insert into mongodb has finished.\n")
    return "files/json_files"

# It takes a taxa string and returns the rank and taxa name
#
# :param taxa: the taxa you want to search for
# :return: A list with the gtdb rank and the taxa name.
def search_gtdb_rank(taxa):
    rank_taxa = taxa.split(sep="__")
    if rank_taxa[0] == 'd':
        rank = "domain"
    elif rank_taxa[0] == 'p':
        rank = "phylum"
    elif rank_taxa[0] == 'c':
        rank = "class"
    elif rank_taxa[0] == 'o':
        rank = "order"
    elif rank_taxa[0] == 'f':
        rank = "family"
    elif rank_taxa[0] == 'g':
        rank = "genus"
    elif rank_taxa[0] == 's':
        rank = "species"
    return [rank, rank_taxa[-1]]


# It takes a word as an input, searches the dataframe for that word, and returns the rank of the word if it is found
#
# :param word_to_search: the word you want to search for
# :return: The rank of the taxa or " " if null
def search_rank(word_to_search):
    line = dataframe.loc[dataframe['Taxa_Name'] == word_to_search, ['Taxa_Rank']]
    if line.empty:
        return " "
    rank = line['Taxa_Rank'].values[0]
    return rank


# It takes a line of text, splits it into a list of words, and returns the last word
#
# :param line: the line of text that we're processing
# :return: The final word in the line.
def get_final_word(line):
    res = line.split(sep='	')
    final_word = res[-1]
    return final_word


# It takes a line of text, splits it into a list of words, and returns the first word
#
# :param line: the line of text that we're processing
# :return: The first word in the line.
def get_first_word(word):
    res = word.split(sep='	')
    first_word = res[0]
    return first_word


# It takes a line of text, splits it into a list of words, takes the first word, and returns it
#
# :param line: the line of text that we're reading in
# :return: The first word (taxa) in the line.
def get_first_taxa(line):
    word = line.split(sep=';')[0].strip()
    return word


# It takes a txt file (with the organisms info) as input, and writes a json file as output
#
#     :param file: the file to be read
#     :param output: the file you want to write to
def create_file_json(file, output):
    output.write('[')
    lines = file.readlines()[1:]
    c = 0
    for line in lines:
        if c == 0:
            output.write("{")
        else:
            output.write(',{')
        obj1 = RnaObject(line)
        obj1.add_taxonomy_ena()
        obj1.add_taxonomy_gtdb()
        obj1.add_taxonomy_ltp()
        obj1.add_taxonomy_ncbi()
        obj1.add_taxonomy_silva()
        if obj1.add_accession_number() == -1:
            obj1.accession_number = "--"
        # obj1.add_strain()
        output.write('\"Organism name\": \"' + obj1.organism_name + '\",')
        output.write('\"Accession number\": \"' + obj1.accession_number + '\",')
        if obj1.s_len == "--":
            output.write('\"Length\": \"' + obj1.s_len + '\",')
        else:
            output.write('\"Length\": ' + obj1.s_len + ',')
        if obj1.num_decoupled == "--":
            output.write('\"Number of decoupled nucleotides\": \"' + obj1.num_decoupled + '\",')
        else:
            output.write('\"Number of decoupled nucleotides\": ' + obj1.num_decoupled + ',')
        if obj1.num_weak_bonds == "--":
            output.write('\"Number of weak bonds\": \"' + obj1.num_weak_bonds + '\",')
        else:
            output.write('\"Number of weak bonds\": ' + obj1.num_weak_bonds + ',')
        output.write('\"Is Pseudoknotted\": \"' + obj1.pseudo_knotted + '\",')
        if obj1.pseudo_order == "--":
            output.write('\"Pseudoknot order\": \"' + obj1.pseudo_order + '\",')
        else:
            output.write('\"Pseudoknot order\": ' + obj1.pseudo_order + ',')
        output.write("\n")
        output.write('\"Rna Type\": \"' + obj1.rna_type + '\",')
        if obj1.genus == "--":
            output.write('\"Genus\": \"' + obj1.genus + '\",')
        else:
            output.write('\"Genus\": ' + obj1.genus + ',')
        output.write('\"Core\": \"' + obj1.core + '\",')
        output.write('\"Core plus\": \"' + obj1.core_plus + '\",')
        output.write('\"Shape\": \"' + obj1.shape + '\",')
        output.write('\"Is Validated\": \"' + obj1.is_validated + '\",')
        output.write('\"Reference database\": \"' + obj1.db_name + '\",')
        output.write('\"Description\": \"' + obj1.description + '\",')
        output.write('\"Benchmark ID\": \"' + obj1.benchmark_id + '\",')
        output.write('\"Reference\": \"' + obj1.reference + '\",')
        output.write('\"Taxonomy\": [{')
        if obj1.silva:
            cont = 0
            cont_no_rank = 0
            cont_unknown = 0
            output.write('\"SILVA\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.silva_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.silva_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown " + str(cont_unknown)
                    cont_unknown += 1
                elif rank == "no rank":
                    rank = "no rank " + str(cont_no_rank)
                    cont_no_rank +=1
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.silva_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('\"SILVA\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.ena:
            cont = 0
            cont_no_rank = 0
            cont_unknown = 0
            output.write('{\"ENA\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ena_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ena_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown " + str(cont_unknown)
                    cont_unknown += 1
                elif rank == "no rank":
                    rank = "no rank " + str(cont_no_rank)
                    cont_no_rank += 1
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.ena_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('{\"ENA\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.ltp:
            cont = 0
            cont_no_rank = 0
            cont_unknown = 0
            output.write('{\"LTP\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ltp_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ltp_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown " + str(cont_unknown)
                    cont_unknown += 1
                elif rank == "no rank":
                    rank = "no rank " + str(cont_no_rank)
                    cont_no_rank += 1
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.ltp_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('{\"LTP\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.ncbi:
            cont_no_rank = 0
            cont_unknown = 0
            cont = 0
            output.write('{\"NCBI\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ncbi_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ncbi_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown " + str(cont_unknown)
                    cont_unknown += 1
                elif rank == "no rank":
                    rank = "no rank " + str(cont_no_rank)
                    cont_no_rank += 1
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.ncbi_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('{\"NCBI\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.gtdb:
            cont_no_rank = 0
            cont_unknown = 0
            cont = 0
            output.write('{\"GTDB\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.gtdb_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.gtdb_taxonomy.split(sep=';')):
                output.write(',')
                result = search_gtdb_rank(taxa)
                rank = result[0]
                taxa = result[1]
                if rank == " ":
                    rank = "unknown " + str(cont_unknown)
                    cont_unknown += 1
                elif rank == "no rank":
                    rank = "no rank " + str(cont_no_rank)
                    cont_no_rank += 1
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.gtdb_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}}")
        else:
            output.write('{\"GTDB\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}}")
        output.write("]}")
        print(c)
        c += 1
    output.write("]")


