
import os
import argparse
import time
import lda
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
from lda_tsne_model2 import lda_tsne
import time
import os
from compressed_main import stem
from compressed_main import tokenize_and_stem
from extractor import extract
from sklearn.decomposition import LatentDirichletAllocation


totalvocab_stemmed = []
totalvocab_tokenized = []
total_text = []
file_names = []

t0 = time.time()

for filename in os.listdir('uploads/extracted/better_test'):
    mypath = 'uploads/extracted/better_test'
    text, tokens, keywords = extract(os.path.join(mypath, filename))
    totalvocab_stemmed.extend(stem(tokens))
    totalvocab_tokenized.extend(tokens)
    total_text.append(text)
    file_names.append(filename)


n_data = len(file_names)

n_topics =  int(round(((len(file_names))/2)**0.5))
n_iter = 200
n_top_words = 5
threshold = 0.5

t0 = time.time()


cvectorizer = CountVectorizer(min_df=1, stop_words='english')
cvz = cvectorizer.fit_transform(total_text)




lda_model = lda.LDA(n_topics=n_topics, n_iter=10)
X_topics = lda_model.fit_transform(cvz)
topic_word = lda_model.topic_word_


lda_model2 = LatentDirichletAllocation(n_components=n_topics)
X_topics2 = lda_model2.fit_transform(cvz)
topic_word2 = lda_model2.components_ 

print(((topic_word==topic_word2).all()))

print(X_topics)
print(X_topics2)