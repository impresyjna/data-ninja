# -*- coding: utf-8 -*-
import time
import numpy as np
import pandas as pd
import glob
import operator

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

t0 = time.time()
categories = pd.read_csv(categories_file, sep="\t", header=None, skiprows=[0,1]).values
print("Czas wczytywania w s: " + str(time.time()-t0))

print(categories[:,0].size)
print(frame[:,0].size)

# Get bags of 100 most popular words
titles = frame[:,1]
words = []
for title in titles:
    title = title.replace(',', '')
    string_words = title.split()
    for word in string_words:
        if(len(word) > 2):
            words.append(word)
classes = {}
for value in set(words):
    classes[value] = 0
for value in words:
    classes[value] += 1
sorted_words = sorted(classes.items(), key=operator.itemgetter(1))[-100:]
print(len(sorted_words))