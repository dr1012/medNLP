import os
import argparse
import time
from sklearn.decomposition import LatentDirichletAllocation
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
from flask import session
import pandas as pd
from stopwords import stop_word_list
import pickle
import lda
from extractor import extract
import seaborn as sns
import matplotlib.pyplot as plt

total_text = ['My name is David Rudolf, I grew up in France.', 'My hobbies are surfing, skiing, computer science.', 'I used to study physics, now I study computer science', '"Hello my fucking friends!', "what a wonderful world this is, don't you think? I thought this too!"]



stopwords = stop_word_list()

cvectorizer = CountVectorizer(min_df=1, stop_words=stopwords,  lowercase = True, ngram_range = (1,3))
cvz = cvectorizer.fit_transform(total_text)

print(cvectorizer.get_feature_names())
print(cvz.toarray())
lda_model = LatentDirichletAllocation(n_components=3)
#lda_model = lda.LDA(n_topics, 200 )

X_topics = lda_model.fit_transform(cvz)

print(X_topics)


tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.50,
                    init='pca')
tsne_lda = tsne_model.fit_transform(X_topics)

print(tsne_lda)

_lda_keys = []
for i in range(X_topics.shape[0]):
    print(X_topics[i])
    print(X_topics[i].argmax())
    _lda_keys += X_topics[i].argmax(),

print(_lda_keys)



palette = sns.color_palette('deep', len(_lda_keys))
colors = [palette[x] for x in _lda_keys]
plt.scatter(tsne_lda[:,0], tsne_lda[:,1])
plt.show()
