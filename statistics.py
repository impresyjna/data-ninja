import time
import numpy as np
import pandas as pd
import sys
import glob

categories_file = "categories.tsv"

test_path = "test"
allFiles = glob.glob(test_path + "/*.tsv")
frame = pd.DataFrame()
list_ = []
t0 = time.time()
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=None, sep="\t")
    list_.append(df)
frame = pd.concat(list_)
frame = frame.values

categories = pd.read_csv(categories_file, sep="\t", header=None, skiprows=[0,1]).values
print("Liczba kategorii " + categories[:,0].size)
print(frame[:,0].size)


