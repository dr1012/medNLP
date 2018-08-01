

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
import bokeh.plotting as bp
from bokeh.plotting import save, output_file, show
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html
import random
from bokeh.embed import components
from stopwords import stop_word_list
import hdbscan
from extractor import extract
import os
from compressed_main import stem, tokenize_and_stem
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

from yellowbrick.text import TSNEVisualizer

from yellowbrick.style.palettes import PALETTES, SEQUENCES, color_palette

import yellowbrick


totalvocab_stemmed = []
totalvocab_tokenized = []
total_text = []
file_names = []

t0  = time.time()

for filename in os.listdir('uploads/extracted/full_test'):
    mypath = 'uploads/extracted/full_test'
    text, tokens, keywords = extract(os.path.join(mypath, filename))
    totalvocab_stemmed.extend(stem(tokens))
    totalvocab_tokenized.extend(tokens)
    total_text.append(text)
    file_names.append(filename)


t1 = time.time()

print("time to import docs: " + str(t1-t0))



n_docs = len(file_names)
stopwords = stop_word_list()




t6 = time.time()

countvec = TfidfVectorizer(max_df=1.0, min_df=1,  lowercase = True, stop_words=stopwords, ngram_range=(1,3))
cvz = countvec.fit_transform(total_text)

t7 = time.time()

print("time to count vectorize: " + str(t7-t6))

clusterer = hdbscan.HDBSCAN(min_cluster_size=7)
result = clusterer.fit_predict(cvz)
t8 = time.time()

print("time for hdbscan: " + str(t8-t7))

print(result)

n_topics2= np.unique(result).max()+1

print("number of topics with count vec: " + str(n_topics2))