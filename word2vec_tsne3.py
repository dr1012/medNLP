import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
import re
import nltk
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import matplotlib as mpl
from wordcloud import WordCloud, STOPWORDS
from stopwords import stop_word_list
from pdf_extractor import extract

import spacy

stop_words =  stop_word_list()


text, tokens, keywords = extract('uploads/mytest.pdf')


for word in tokens:
    if word in stop_words:
        tokens.remove(word)  

cleantext = " ".join(tokens)



nlp = spacy.load('en_core_web_sm')  # make sure to use larger model!

doc = nlp(cleantext)
list_of_lists = []
for sentence in doc.sents:
    inner_list = []
    for token in sentence:
        inner_list.append(token.text)
    list_of_lists.append(inner_list) 
        




model = word2vec.Word2Vec(list_of_lists, size=100, window=10, min_count=1, workers=4)



embeddings = model.wv








import sys, os
import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins.projector import visualize_embeddings, ProjectorConfig
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



def visualize(model, output_path):
    meta_file = "w2x_metadata.tsv"
    placeholder = np.zeros((len(model.wv.index2word), 100))

    with open(os.path.join(output_path,meta_file), 'wb') as file_metadata:
        for i, word in enumerate(model.wv.index2word):
            placeholder[i] = model[word]
            # temporary solution for https://github.com/tensorflow/tensorflow/issues/9094
            if word == '':
                print("Emply Line, should replecaed by any thing else, or will cause a bug of tensorboard")
                file_metadata.write("{0}".format('<Empty Line>').encode('utf-8') + b'\n')
            else:
                file_metadata.write("{0}".format(word).encode('utf-8') + b'\n')

  
    config = tf.ConfigProto(device_count = {'GPU': 0})
    
    # define the model without training
    sess = tf.InteractiveSession(config=config)



    embedding = tf.Variable(placeholder, trainable = False, name = 'w2x_metadata')
    tf.global_variables_initializer().run()

    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(output_path, sess.graph)

    # adding into projector
    config = ProjectorConfig()
    embed = config.embeddings.add()
    embed.tensor_name = 'w2x_metadata'
    embed.metadata_path = meta_file


    # Specify the width and height of a single thumbnail.
    visualize_embeddings(writer, config)
    saver.save(sess, os.path.join(output_path,'w2x_metadata.ckpt'))
    print('Run `tensorboard --logdir={0}` to run visualize result on tensorboard'.format(output_path))
    

output_path =  'tensorflow_viz'

visualize(model, output_path)






