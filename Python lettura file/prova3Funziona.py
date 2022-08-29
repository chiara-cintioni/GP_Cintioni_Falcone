

import pandas as pd

inputFile = input("Insert file name with file extension (txt) to modify: ")
outputFile = input("Insert file name with file extension (csv) where saves file raws without duplicates: ")
data = pd.read_table(inputFile, low_memory=False)
data.drop_duplicates(['submitted_name'], keep='last').to_csv(outputFile, sep='	')






