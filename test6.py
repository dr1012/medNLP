from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import lda

data = ['blah blah foo bar', 'foo foo foo foo bar', 'bar bar bar bar foo',
        'foo bar bar bar baz foo', 'foo foo foo bar baz', 'blah banana', 
        'cookies candy', 'more text please', 'hey there are more words here',
        'bananas', 'i am a real boy', 'boy', 'girl']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data)

vocab = vectorizer.get_feature_names()

n_top_words = 5
k = 2

lda_model = lda.LDA(k, 200 )

id_topic = lda_model.fit_transform(X)

topic_words = {}






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

