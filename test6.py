from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

data = ['blah blah foo bar', 'foo foo foo foo bar', 'bar bar bar bar foo',
        'foo bar bar bar baz foo', 'foo foo foo bar baz', 'blah banana', 
        'cookies candy', 'more text please', 'hey there are more words here',
        'bananas', 'i am a real boy', 'boy', 'girl']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data)

vocab = vectorizer.get_feature_names()

n_top_words = 5
k = 2

model = LatentDirichletAllocation(n_topics=k, random_state=100)

id_topic = model.fit_transform(X)

topic_words = {}

print(model.components_)
print()
print(id_topic)