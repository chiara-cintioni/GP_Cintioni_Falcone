# Read Text Files with Pandas using read_table()
import hashlib

# importing pandas
import pandas as pd


data = pd.read_table("taxmap.txt", low_memory=False)

data.drop_duplicates(['submitted_path','submitted_name'], keep = 'last').to_csv("out.csv", sep=' ')





