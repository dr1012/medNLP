#http://nbviewer.jupyter.org/github/bmabey/hacker_news_topic_modelling/blob/master/HN%20Topic%20Model%20Talk.ipynb#topic=1&lambda=1&term=
#http://nbviewer.jupyter.org/github/bmabey/pyLDAvis/blob/master/notebooks/pyLDAvis_overview.ipynb

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import os
from extractor import extract
from compressed_main import stem
from compressed_main import tokenize_and_stem
from stopwords import stop_word_list
import numpy as np
import pyLDAvis
from pyLDAvis.sklearn import prepare
import tqdm
import time
import pickle
import os 

def pyladvis_run(lda_model_path, document_term_matrix_path, vectorizer_path):

    t0 = time.time()

    lda_model = pickle.load( open(lda_model_path, "rb" ) )
    document_term_matrix = pickle.load( open(document_term_matrix_path, "rb" ) )
    cvectorizer = pickle.load( open(vectorizer_path, "rb" ) )
 
    prepared_data = prepare(lda_model,document_term_matrix,cvectorizer, mds = 'tsne', plot_opts={'xlab': '', 'ylab': ''})


    html = pyLDAvis.prepared_data_to_html(prepared_data)

    #os.remove(lda_model_path)
    #os.remove(document_term_matrix)
    #os.remove(vectorizer_path)

    t1 = time.time()
    print("time for pyldavis: " + str(t1-t0))

    return html



# might be needed for having a list of topic summaries table next to the circles
'''
topic_words = {}
n_top_words = 5
k = 2
for topic, comp in enumerate(lda_model.components_):
    # for the n-dimensional array "arr":
    # argsort() returns a ranked n-dimensional array of arr, call it "ranked_array"
    # which contains the indices that would sort arr in a descending fashion
    # for the ith element in ranked_array, ranked_array[i] represents the index of the
    # element in arr that should be at the ith index in ranked_array
    # ex. arr = [3,7,1,0,3,6]
    # np.argsort(arr) -> [3, 2, 0, 4, 5, 1]
    # word_idx contains the indices in "topic" of the top num_top_words most relevant
    # to a given topic ... it is sorted ascending to begin with and then reversed (desc. now)    
    word_idx = np.argsort(comp)[::-1][:n_top_words]
    # store the words most relevant to the topic
    topic_words[topic] = [vocab[i] for i in word_idx]
for topic, words in topic_words.items():
    print('Topic: %d' % topic)
    print('  %s' % ', '.join(words))
'''