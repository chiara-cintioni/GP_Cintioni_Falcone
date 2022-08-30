file = open('files/taxmap_ENA.txt', 'r')
output_dup = open('files/reduced_taxmap.txt', 'w')

import hashlib
import pandas as pd

def reduce_file():
    inputFile = input("Insert file name with file extension (txt) to modify: ")
    outputFile = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    data = pd.read_table(inputFile, low_memory=False)
    data.drop_duplicates(['submitted_name'], keep = 'last').to_csv(outputFile, sep='	')


def reduce_file2():
    inputFile = input("Insert file name with file extension (txt) to modify: ")
    outputFile = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    data = pd.read_table(inputFile, low_memory=False)
    data.drop_duplicates(['organism_name'], keep = 'last').to_csv(outputFile, sep='	')


def remove_duplicates(file):
    k = []
    for line in file:
        words = line.split('	')
        i = words[4]
        if i not in k:
            k.append(i)
            output_dup.write(line)

reduce_file2()

