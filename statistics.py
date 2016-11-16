# -*- coding: utf-8 -*-
from __future__ import division
import time
import numpy as np
import pandas as pd
import glob
import operator
from itertools import combinations

categories_file = "categories.tsv"

file = open("results.txt", "w")

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
file.write("Czas wczytywania training w s: " + str(time.time()-t0) + "\n")

t0 = time.time()
categories = pd.read_csv(categories_file, sep="\t", header=None, skiprows=[0,1]).values
file.write("Czas wczytywania categories w s: " + str(time.time()-t0)+ "\n")

file.write(str(categories[:,0].size)+ "\n")
file.write(str(frame[:,0].size)+ "\n")

# Get bags of 100 most popular words
t0 = time.time()
titles = frame[:,1]
words = []
denied_words = ["dla", "lub", "bdb", "nowy", "nowa", "okazja", "zł", "bez", "polecam", "zaraz", "sprzedam", "nie", "nowe"]
for title in titles:
    title = title.replace(',', '')
    title = title.replace('/', '')
    title = title.replace(':', '')
    title = title.replace(';', '')
    title = title.replace('?', '')
    title = title.replace('!', '')
    title = title.replace('-', '')
    string_words = title.split()
    for word in string_words:
        if(len(word) > 2 and not all(ch.isdigit() for ch in word.lower()) and not any(word.lower() in s for s in denied_words)):
            words.append(word.lower())

classes = {}
for value in set(words):
    classes[value] = 0
for value in words:
    classes[value] += 1

sorted_words = sorted(classes.items(), key=operator.itemgetter(1))[-100:]
bag_of_words = [x[0] for x in sorted_words]
file.write(str(sorted_words) + "\n")
file.write(str(len(bag_of_words)) + "\n")
file.write("Czas tworzenia bag of words w s: " + str(time.time()-t0)+ "\n")

#filtering data
t0 = time.time()
filtred_data = []
for advert in frame:
    if any(s in advert[1] for s in bag_of_words):
        filtred_data.append(advert)

filtred_data = np.array(filtred_data)
file.write("Czas tworzenia przefiltrowanych danych w s: " + str(time.time()-t0)+ "\n")
file.write(str(filtred_data[:, 0].size) + "\n")

file.write("Rozmiar tabeli trainings " + str(np.array(frame).nbytes) + "\n")
file.write("Rozmiar tabeli filtred_data " + str(filtred_data.nbytes) + "\n")

frame = []
classes = []
sorted_words = []

# # For single word
# t0 = time.time()
# single_words_dictionary = {}
# for value in set(bag_of_words):
#     single_words_dictionary[value] = {}
# for advert in filtred_data:
#     for word in bag_of_words:
#         if(word in advert[1]):
#             if not np.isnan(advert[4]):
#                 if advert[4] in single_words_dictionary[word]:
#                     single_words_dictionary[word][advert[4]] += 1
#                 else:
#                     single_words_dictionary[word][advert[4]] = 1
#             if not np.isnan(advert[5]):
#                 if advert[5] in single_words_dictionary[word]:
#                     single_words_dictionary[word][advert[5]] += 1
#                 else:
#                     single_words_dictionary[word][advert[5]] = 1
#             if not np.isnan(advert[6]):
#                 if advert[6] in single_words_dictionary[word]:
#                     single_words_dictionary[word][advert[6]] += 1
#                 else:
#                     single_words_dictionary[word][advert[6]] = 1
#
# word_ranking = {}
#
# for word in single_words_dictionary:
#     sum_for_word = sum(single_words_dictionary[word].values())
#     word_ranking[word] = sum_for_word
#     single_words_dictionary[word] = sorted(single_words_dictionary[word].items(), key=operator.itemgetter(1))[-3:]
#     file.write(str(word) + "\n")
#     for category in single_words_dictionary[word]:
#         new_category = list(category)
#         new_category.append(float(new_category[1]/sum_for_word))
#         file.write(str(new_category) + "\n")
#
# word_ranking = sorted(word_ranking.items(), key=operator.itemgetter(1))[-30:]
# file.write("\n")
# file.write(str(word_ranking)+"\n")
# file.write("Czas tworzenia grupowania dla pojedynczych slow w s: " + str(time.time()-t0)+ "\n")
#
# #For tuples
# t0 = time.time()
# tuples = ([",".join(map(str, comb)) for comb in combinations(bag_of_words, 2)])
#
# tuples_words_dictionary = {}
# for value in set(tuples):
#     tuples_words_dictionary[value] = {}
#
# index = 0
# for word in tuples:
#     for advert in filtred_data:
#         if(word[0] in advert[1] and word[1] in advert[1]):
#             if not np.isnan(advert[4]):
#                 if advert[4] in tuples_words_dictionary[word]:
#                     tuples_words_dictionary[word][advert[4]] += 1
#                 else:
#                     tuples_words_dictionary[word][advert[4]] = 1
#             if not np.isnan(advert[5]):
#                 if advert[5] in tuples_words_dictionary[word]:
#                     tuples_words_dictionary[word][advert[5]] += 1
#                 else:
#                     tuples_words_dictionary[word][advert[5]] = 1
#             if not np.isnan(advert[6]):
#                 if advert[6] in tuples_words_dictionary[word]:
#                     tuples_words_dictionary[word][advert[6]] += 1
#                 else:
#                     tuples_words_dictionary[word][advert[6]] = 1
#     print(index)
#     index += 1
# word_ranking = {}
#
# for word in tuples_words_dictionary:
#     sum_for_word = sum(tuples_words_dictionary[word].values())
#     word_ranking[word] = sum_for_word
#     tuples_words_dictionary[word] = sorted(tuples_words_dictionary[word].items(), key=operator.itemgetter(1))[-3:]
#     file.write(str(word) + "\n")
#     for category in tuples_words_dictionary[word]:
#         new_category = list(category)
#         new_category.append(float(new_category[1]/sum_for_word))
#         file.write(str(new_category) + "\n")
#
# word_ranking = sorted(word_ranking.items(), key=operator.itemgetter(1))[-30:]
# file.write("\n")
# file.write(str(word_ranking)+"\n")
# file.write("Czas tworzenia grupowania danych dla tupli w s: " + str(time.time()-t0) + "\n")

file.close()
#Grupowanie (2.5.1)
#Wyszukiwanie najbliższych sąsiadów (2.5.2)

