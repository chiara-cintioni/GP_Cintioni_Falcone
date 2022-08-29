import pandas as pd


def search_rank_ncbi_ena(rank_to_search):
    rank_file = open("files/TaxaName_TaxaRank.txt", "r")
    rank_file_lines = rank_file.readlines()
    for line in rank_file_lines:
        first_word = get_first_word(line).strip()
        if rank_to_search == first_word:
            rank = get_final_word(line).strip()
            rank_file.close()
            return rank
    rank_file.close()
    return " "


def get_final_word(word):
    res = word.split(sep='	')
    final_word = res[len(res)-1]
    return final_word


def get_first_word(word):
    res = word.split(sep='	')
    first_word = res[0]
    return first_word


# class that creates a RnaObject that contains all the info
# make it possible to add more taxonomies
class RnaObject:

    def __init__(self, info):
        elements = info.split(sep="	")
        cont = 0
        self.silva = False
        self.silva_taxonomy = ''
        self.ena = False
        self.ena_taxonomy = ''
        self.ltp = False
        self.ltp_taxonomy = ''
        self.ncbi = False
        self.ncbi_taxonomy = ''
        self.gtdb = False
        self.gtdb_taxonomy = ''
        for element in elements:
            if cont == 0:
                self.organism_name = element
                cont += 1
            elif cont == 1:
                self.benchmark_id = element
                cont += 1
            elif cont == 2:
                self.length = element
                cont += 1
            elif cont == 3:
                self.num_weak_bonds = element
                cont += 1
            elif cont == 4:
                self.num_decoupled = element
                cont += 1
            elif cont == 5:
                self.pseudo_knotted = element
                cont += 1
            elif cont == 6:
                self.rna_type = element
                cont += 1
            elif cont == 7:
                self.genus = element
            elif cont == 8:
                self.core = element
            elif cont == 9:
                self.core_plus = element
            elif cont == 10:
                self.shape = element

    def add_taxonomy_silva(self):
        """
        If the organism name is not found in the LSU database, then check the SSU database. If it's not found in the SSU
        database, then set the silva attribute to False. If it is found in either database, then set the silva attribute to
        True and set the silva_taxonomy attribute to the taxonomy path
        """
        lsu_silva_taxonomy = open('files/silva/silva_lsu_taxonomy.txt', 'r')
        ssu_silva_taxonomy = open('files/silva/silva_ssu_taxonomy.txt', 'r')
        df = pd.read_table(lsu_silva_taxonomy)
        line = df.loc[df['organism_name'] == self.organism_name, ['path']]
        empty_df = pd.DataFrame(columns=['path'])
        if empty_df.equals(line):
            df = pd.read_table(ssu_silva_taxonomy)
            line = df.loc[df['organism_name'] == self.organism_name, ['path']]
            if empty_df.equals(line):
                self.silva = False
            else:
                self.silva = True
                self.silva_taxonomy = str(line)
        else:
            self.silva = True
            self.silva_taxonomy = str(line)

    def add_taxonomy_ena(self):
        """
                If the organism name is in the lsu_ena_taxonomy file, then the ena_taxonomy is set to the line in the file that
                contains the organism name. If the organism name is not in the lsu_ena_taxonomy file, then the function checks the
                ssu_ena_taxonomy file. If the organism name is in the ssu_ena_taxonomy file, then the ena_taxonomy is set to the
                line in the file that contains the organism name. If the organism name is not in the ssu_ena_taxonomy file, then the
                ena variable is set to False
                """
        lsu_ena_taxonomy = open('files/ena/ena_lsu_ref_nr99.txt', 'r')
        ssu_ena_taxonomy = open('files/ena/ena_ssu_ref_nr99.txt', 'r')
        df = pd.read_table(lsu_ena_taxonomy)
        line = df.loc[df['submitted_name'] == self.organism_name, ['submitted_path']]
        empty_df = pd.DataFrame(columns=['submitted_path'])
        if empty_df.equals(line):
            df = pd.read_table(ssu_ena_taxonomy)
            line = df.loc[df['submitted_name'] == self.organism_name, ['submitted_path']]
            if empty_df.equals(line):
                self.ena = False
            else:
                self.ena = True
                self.ena_taxonomy = str(line)
        else:
            self.ena = True
            self.ena_taxonomy = str(line)

    def add_taxonomy_ltp(self):
        """
        This function takes the organism name of a given object and searches for it in a dataframe of the LTP taxonomy. If
        the organism name is found, the function returns True and the taxonomy of the organism. If the organism name is not
        found, the function returns False
        """
        ltp_taxonomy = open('files/ltp/LTP_taxonomy.txt', 'r')
        df = pd.read_table(ltp_taxonomy)
        line = df.loc[df['organism_name'] == self.organism_name, ['path']]
        empty_df = pd.DataFrame(columns=['path'])
        if empty_df.equals(line):
            self.ltp = False
        else:
            self.ltp = True
            self.ltp_taxonomy = str(line)

    def add_taxonomy_ncbi(self):
        """
        If the organism name is in the LSU database, then the taxonomy is added to the object. If it's not in the LSU
        database, then the SSU database is checked. If it's not in the SSU database, then the NCBI taxonomy is set to False
        """
        lsu_ncbi_taxonomy = open('files/ncbi/ncbi_lsu_ref_nr99.txt', 'r')
        ssu_ncbi_taxonomy = open('files/ncbi/ncbi_ssu_ref_nr99.txt', 'r')
        df = pd.read_table(lsu_ncbi_taxonomy)
        line = df.loc[df['submitted_name'] == self.organism_name, ['submitted_path']]
        empty_df = pd.DataFrame(columns=['submitted_path'])
        if empty_df.equals(line):
            df = pd.read_table(ssu_ncbi_taxonomy)
            line = df.loc[df['submitted_name'] == self.organism_name, ['submitted_path']]
            if empty_df.equals(line):
                self.ncbi = False
            else:
                self.ncbi = True
                self.ncbi_taxonomy = str(line)
        else:
            self.ncbi = True
            self.ncbi_taxonomy = str(line)

    def add_taxonomy_gtdb(self):
        """
        If the organism name is in the bacteria file, then the taxonomy is added to the object. If not, then it checks the
        archaea file. If it's not in the archaea file, then the gtdb attribute is set to False
        """
        bacteria_gtdb_taxonomy = open('files/gtdb/gtdb_bacteria.txt', 'r')
        archaea_gtdb_taxonomy = open('files/gtdb/gtdb_archaea.txt', 'r')
        df = pd.read_table(bacteria_gtdb_taxonomy)
        line = df.loc[df['ncbi_organism_name'] == self.organism_name, ['gtdb_taxonomy']]
        empty_df = pd.DataFrame(columns=['gtdb_taxonomy'])
        if empty_df.equals(line):
            df = pd.read_table(archaea_gtdb_taxonomy)
            line = df.loc[df['ncbi_organism_name'] == self.organism_name, ['gtdb_taxonomy']]
            if empty_df.equals(line):
                self.gtdb = False
            else:
                self.gtdb = True
                self.gtdb_taxonomy = str(line)
        else:
            self.gtdb = True
            self.gtdb_taxonomy = str(line)


def get_first_silva_taxa(line):
    word = line.split(sep=';')[0].strip()
    return word.split(sep=" ")[-1]


def create_json():
    file = open('files/rna_sequences/Archaea23S.txt', 'r')
    output = open('files/result_json.json', 'w')
    output.write('[')
    lines = file.readlines()[1:]
    c = 0
    for line in lines:
        if c==0:
            output.write("{")
        else:
            output.write(',{')
        obj1 = RnaObject(line)
        obj1.add_taxonomy_ena()
        obj1.add_taxonomy_gtdb()
        obj1.add_taxonomy_ltp()
        obj1.add_taxonomy_ncbi()
        obj1.add_taxonomy_silva()
        output.write('\"Organism name\": \"' + obj1.organism_name + '\",')
        output.write('\"Length\": ' + obj1.length + ',')
        output.write('\"Number of decoupled nucleotides\": ' + obj1.num_decoupled + ',')
        output.write('\"Number of weak bonds\": ' + obj1.num_weak_bonds + ',')
        output.write('\"Is Pseudoknotted\": \"' + obj1.pseudo_knotted + '\",')
        output.write('\"Rna Type\": \"' + obj1.rna_type + '\",')
        output.write('\"Taxonomy\": [{')
        if obj1.silva:
            cont = 0
            output.write('\"SILVA\": {')
            output.write('\"Classified\": \"Yes\"')
            taxa = get_first_silva_taxa(obj1.silva_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.silva_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank_ncbi_ena(taxa)
                if rank == " ":
                    rank = "no rank"
                output.write('\"'+rank+'\": \"'+taxa+'\"')
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
            taxa = get_first_silva_taxa(obj1.silva_taxonomy)
            cont += 1
            while taxa != "" and cont < len(obj1.silva_taxonomy.split(sep=';')):
                output.write(',')
                rank = search_rank_ncbi_ena(taxa)
                if rank == " ":
                    rank = "no rank"
                output.write('\"' + rank + '\": \"' + taxa + '\"')
                taxa = obj1.silva_taxonomy.split(sep=';')[cont]
                cont += 1
            output.write("}}")
        else:
            output.write('{\"ENA\": {')
            output.write('\"Classified\": \"No\"')
            output.write("}}")
        output.write("]}")
        c += 1
    output.write("]")

# pass lines from file
# reduce_file2()
# i = "Haloarcula marismortui	CRW-23S_A_E_1	2925	852	4146	Yes	23S"
# obj1 = RnaObject(i)
# obj1.add_taxonomy_ena()
# print(obj1.organism_name)
create_json()
# search_rank_NCBI_ENA("Peduovirus")
# example1 = "Questa   frase   è   un  esempio per vedere  se  prende  la  prima   parola"
# print(get_final_word(example1))
# search_rank_NCBI_ENA()
# create_json()
# print(data)