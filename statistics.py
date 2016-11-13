import time
import numpy as np
import pandas as pd
import sys

categories_file = "categories.tsv"

categories = pd.read_csv(categories_file, sep="\t", header=None, skiprows=[0,1]).values
print(categories[:,0].size)


