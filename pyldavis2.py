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

stopwords = stop_word_list()


totalvocab_stemmed = []
totalvocab_tokenized = []
total_text = []
file_names = []

t0 = time.time()

for filename in os.listdir('uploads/extracted/medium_test'):
    mypath = 'uploads/extracted/medium_test'
    text, tokens, keywords = extract(os.path.join(mypath, filename))
    totalvocab_stemmed.extend(stem(tokens))
    totalvocab_tokenized.extend(tokens)
    total_text.append(text)
    file_names.append(filename)

t1 = time.time()

print('time for text extraction from files: ' + str((t1-t0)))

vectorizer = CountVectorizer(stop_words = stopwords,
                                lowercase = True,
                                ngram_range = (1,2), 
                                min_df = 1,
                                max_df = 30)


# X = docuemnt-term matrix
X = vectorizer.fit_transform(total_text)

t2 = time.time()


print('time for count vectorizer: ' + str((t2-t1)))

#vocab = vectorizer.get_feature_names()

n_top_words = 5

lda_model = LatentDirichletAllocation(n_components=17, random_state=100)
lda_model.fit_transform(X)

t3 = time.time()

print('time for LDA: ' + str((t3-t2)))

prepared_data = prepare(lda_model,X,vectorizer, mds = 'tsne', plot_opts={'xlab': '', 'ylab': ''})

 
t4 = time.time()



print('time for pyLDAvis: ' + str((t4-t3)))
print('total time: ' + str((t4-t0)))
 





#html = pyLDAvis.prepared_data_to_html(prepared_data)

#Html_file= open("pyLDAvis_test.html","w")
#Html_file.write(html)
#Html_file.close()

pyLDAvis.show(prepared_data)



'''
topic_words = {}

for topic, comp in enumerate(model.components_):
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