from create_rna_object import RnaObject


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


def search_rank(word_to_search):
    rank_file = open("files/taxonomy/TaxaName_TaxaRank.txt", "r")
    rank_file_lines = rank_file.readlines()
    for line in rank_file_lines:
        first_word = get_first_word(line).strip()
        if word_to_search == first_word:
            rank = get_final_word(line).strip()
            rank_file.close()
            return rank
    rank_file.close()
    return " "


def get_final_word(line):
    res = line.split(sep='	')
    final_word = res[-1]
    return final_word


def get_first_word(word):
    res = word.split(sep='	')
    first_word = res[0]
    return first_word


def get_first_taxa(line):
    word = line.split(sep=';')[0].strip()
    return word.split(sep=" ")[-1]


"""
def get_domain(obj1):
    taxa = get_first_taxa(obj1.silva_taxonomy)
    cont = 0
    domain = ''
    while taxa != "" and cont < len(obj1.silva_taxonomy.split(sep=';')):
        rank = search_rank(taxa)
        if rank == "superkingdom":
            domain = taxa
            return domain
    taxa = get_first_taxa(obj1.ena_taxonomy)
    cont = 0
    while taxa != "" and cont < len(obj1.ena_taxonomy.split(sep=';')):
        rank = search_rank(taxa)
        if rank == "superkingdom":
            domain = taxa
            return domain
    taxa = get_first_taxa(obj1.ltp_taxonomy)
    cont = 0
    while taxa != "" and cont < len(obj1.ltp_taxonomy.split(sep=';')):
        rank = search_rank(taxa)
        if rank == "superkingdom":
            domain = taxa
            return domain
    taxa = get_first_taxa(obj1.ncbi_taxonomy)
    cont = 0
    while taxa != "" and cont < len(obj1.ncbi_taxonomy.split(sep=';')):
        rank = search_rank(taxa)
        if rank == "superkingdom":
            domain = taxa
            return domain
    taxa = get_first_taxa(obj1.gtdb_taxonomy)
    cont = 0
    while taxa != "" and cont < len(obj1.gtdb_taxonomy.split(sep=';')):
        rank = search_rank(taxa)
        if rank == "domain":
            domain = taxa
            return domain
    return "unknown"
"""

def create_file_json(file, output, file_path):
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
        # obj1.db_name da inserire al posto di CRW
        output.write('\"Reference database\": \"' + obj1.db_name + '\",')
        # obj1.link_db da inserire al posto del link diretto
        output.write('\"Reference database link\": \"' + obj1.link_db + '\",')
        output.write('\"Benchmark ID\": \"' + obj1.benchmark_id + '\",')
        output.write('\"Taxonomy\": [{')
        if obj1.silva:
            cont = 0
            output.write('\"SILVA\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.silva_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.silva_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown"
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
            output.write('{\"ENA\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ena_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ena_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown"
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
            output.write('{\"LTP\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ltp_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ltp_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown"
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.ltp_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('{\"LTP\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.ncbi:
            cont = 0
            output.write('{\"NCBI\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_taxa(obj1.ncbi_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.ncbi_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank(taxa)
                if rank == " ":
                    rank = "unknown"
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.ncbi_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}},")
        else:
            output.write('{\"NCBI\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}},")
        if obj1.gtdb:
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
                if rank == "":
                    rank = "unknown"
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



