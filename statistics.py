import time
import numpy as np
import pandas as pd
import sys
import glob

categories_file = "categories.tsv"

test_path = "training.v2"
allFiles = glob.glob(test_path + "/training.*.tsv")
frame = pd.DataFrame()
list_ = []
t0 = time.time()
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=None, sep="\t", names=list(range(7)))
    list_.append(df)
frame = pd.concat(list_)
frame = frame.values
print("Czas wczytywania w s: " + str(time.time()-t0))

categories = pd.read_csv(categories_file, sep="\t", header=None, skiprows=[0,1]).values
print(categories[:,0].size)
print(frame[:,0].size)


