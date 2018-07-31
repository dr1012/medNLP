

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




t2 = time.time()
tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1,  lowercase = True, stop_words=stopwords, ngram_range=(1,2))

tfidf_matrix = tfidf_vectorizer.fit_transform(total_text) #fit the vectorizer to synopses

t3 = time.time()

print("time to import vectorizer and vectorize text: " + str(t3-t2))

#all the different n-grams in the texts
#terms = tfidf_vectorizer.get_feature_names()



#clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
#result = clusterer.fit_predict(tfidf_matrix)


X = tfidf_matrix.todense()
t4 = time.time()

print("time to convert tf idf sparse matrix to dense matkrix: " + str(t4-t3))

labels, probabilities,cluster_persistence,condensed_tree,single_linkage_tree,min_spanning_tree  = hdbscan.hdbscan(X = X, min_cluster_size=4)

t5 = time.time()

print("time to apply HDBSCAN: " + str(t5-t4))

'''
print(labels)
print()
print(probabilities)
print()
print(cluster_persistence)
print()
print(condensed_tree)
print()
print(single_linkage_tree)
print()
print(min_spanning_tree)
'''

#x = hdbscan.plots.CondensedTree(condensed_tree)

#x.plot()

#plt.show()

##################################################################################



n_topics = np.unique(labels).max()+1

print(n_topics)


prob_matrix = np.zeros((n_docs, n_topics))

print(prob_matrix.shape)

for i in range(len(probabilities)):
    topic = labels[i]
    if topic >= 0:
        prob_matrix[i][topic] = probabilities[i]


'''
# t-SNE: 50 -> 2D
tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.5,
                    init='pca')

tsne_lda = tsne_model.fit_transform(prob_matrix)
'''


palette = sns.color_palette('deep', np.unique(labels).max() + 1)
palette2 = color_palette('bold', np.unique(labels).max() + 1)
mycolors = [palette[x] if x >= 0.0 else (0.0, 0.0, 0.0) for x in labels]
'''
plt.scatter(tsne_lda[:,0], tsne_lda[:,1], c=colors)
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.show()
'''


colormap =  []
big_colormap = []

mycolormap = yellowbrick.style.colors.resolve_colors(n_colors=n_topics+1, colormap=None, colors=None)

for i  in  range(n_topics):
    if labels[i]>=0:
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        colormap.append(color)
    else:
        color = "#000000"
        colormap.append(color)

for label in labels:
    big_colormap.append(mycolormap[label])



t6 = time.time()






tsne = TSNEVisualizer(colormap='RdYlGn')
tsne.fit(tfidf_matrix, labels)
tsne.poof()

t7 = time.time()

print("time for TSNE and vis: " + str(t7-t6))


tsne.poof()





