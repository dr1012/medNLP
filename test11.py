import os
from extractor import extract


import time
#from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

import random

import pandas as pd
from stopwords import stop_word_list

import lda



apath = r'C:\Users\David\Desktop\meddoc\text_files2'
original_clusters = []
for filename in os.listdir(apath):
    path = os.path.join(apath, filename)

    for x in os.listdir(path):
        afile =  []
        afile.append(x)
        for y in os.listdir(path):
            if y != x:
                afile.append(str(y))
        original_clusters.append(afile)





#####################


total_text = []
file_names = []

all_files = r'C:\Users\David\Desktop\meddoc\text_files'
for filename in os.listdir(all_files):
    text, tokens, keywords = extract(os.path.join(all_files, filename))
    total_text.append(text)
    file_names.append(filename)

############################









n_top_words = 5
n_topics = 40
n_data = len(file_names)



t0 = time.time()

stopwords = stop_word_list()
cvectorizer = CountVectorizer(min_df=1, stop_words=stopwords,  lowercase = True, ngram_range = (1,3))
cvz = cvectorizer.fit_transform(total_text)

t1 = time.time()

print("Time for count vectorizer (document term matrix): " + str(t1-t0))



#lda_model = LatentDirichletAllocation(n_components=n_topics)
t2 = time.time()
lda_model = lda.LDA(n_topics, 500 )

X_topics = lda_model.fit_transform(cvz)

t3=time.time()

print("Time for LDA: " + str(t3-t2))

# print("NUMBER OF ITERATIONS OF LDA: " + str(lda_model.n_iter_))

##############################################################################





num_example = len(X_topics)


_lda_keys = []
for i in range(X_topics.shape[0]):
    _lda_keys += X_topics[i].argmax(),

print("LDA")
print(_lda_keys)
# show topics and their top words
topic_summaries = []
topic_word = lda_model.components_  # get the topic words
vocab = cvectorizer.get_feature_names()
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))

raw_topic_summaries = []
for x in _lda_keys:
    raw_topic_summaries.append(topic_summaries[x])



all_topics = []
for i in range in range(40):
    all_topics.append([])

for j in range(len(_lda_keys)):
    all_topics[_lda_keys[j]].append(file_names[j])


predicted_clusters = []
for x in all_topics:
    for y in x:
        afile =  []
        afile.append(y)
        for z in x:
            if z != y:
                afile.append(z)
    
        predicted_clusters.append(afile)

print(predicted_clusters[0:10])