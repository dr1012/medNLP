from yellowbrick.text import TSNEVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer


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





totalvocab_stemmed = []
totalvocab_tokenized = []
total_text = []
file_names = []

for filename in os.listdir('uploads/extracted/1500'):
    mypath = 'uploads/extracted/1500'
    text, tokens, keywords = extract(os.path.join(mypath, filename))
    totalvocab_stemmed.extend(stem(tokens))
    totalvocab_tokenized.extend(tokens)
    total_text.append(text)
    file_names.append(filename)



n_docs = len(file_names)
stopwords = stop_word_list()

t0 = time.time()
tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1,  lowercase = True, stop_words=stopwords, ngram_range=(1,3))

docs = tfidf_vectorizer.fit_transform(total_text) 

t1 = time.time()



tsne = TSNEVisualizer()
tsne.fit(docs)

t2 = time.time()
print("time for tf idf vectorizer: " + str(t1-t0))
print("time for tsne visualiser: " + str(t2-t1))

tsne.poof()

