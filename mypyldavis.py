#http://nbviewer.jupyter.org/github/bmabey/hacker_news_topic_modelling/blob/master/HN%20Topic%20Model%20Talk.ipynb#topic=1&lambda=1&term=
#http://nbviewer.jupyter.org/github/bmabey/pyLDAvis/blob/master/notebooks/pyLDAvis_overview.ipynb

import os
import pyLDAvis
from pyLDAvis.sklearn import prepare
import time
import pickle


def pyldavis_run(lda_model_path, document_term_matrix_path, vectorizer_path):

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


