#https://shuaiw.github.io/2016/12/22/topic-modeling-and-tsne-visualzation.html
#https://github.com/ShuaiW/twitter-analysis/blob/master/topic_20news.py




import os
import time
#from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
import bokeh.plotting as bp
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html
import random
from flask import session
import pandas as pd
from stopwords import stop_word_list
import pickle
import lda
import flask
from flask import session



def lda_tsne(total_text, file_names, n_topics = None, n_top_words = None):

    myid =  session['myid']

    n_data = len(file_names)

    if n_topics is None:
        n_topics =  int(round(((len(file_names))/2)**0.5))
        session['number_topics'] = str(n_topics)
    
    if n_top_words is None:
        n_top_words = 5
        session['number_topwords'] = str(n_top_words)


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
  

    if not os.path.exists('pickles'):
        os.makedirs('pickles')
    

    lda_model_path = "pickles/lda_model_" + str(myid) + '.p'
    document_term_matrix_path = "pickles/document_term_matrix_" + str(myid) + '.p'
    cvectorizer_path = "pickles/cvectorizer_" + str(myid) + '.p'

    pickle.dump( lda_model, open( lda_model_path, "wb" ) )
    pickle.dump( cvz, open( document_term_matrix_path, "wb" ) )
    pickle.dump( cvectorizer, open( cvectorizer_path, "wb" ) )




   
    ##############################################################################



  

    num_example = len(X_topics)


    t4 =time.time()
    # t-SNE: 50 -> 2D
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.2,
                        init='pca')
    tsne_lda = tsne_model.fit_transform(X_topics[:num_example])

   

    t5 = time.time()


    print("Time for TSNE: " + str(t5-t4))
 

    tsne_lda_df = pd.DataFrame(tsne_lda)

    print(tsne_lda_df.describe())

    tsne_lda_df = tsne_lda_df.fillna('')

    tsne_lda = tsne_lda[~np.isnan(tsne_lda).any(axis=1)]

    tsne_lda_df = tsne_lda_df[~tsne_lda_df.isin([np.nan, np.inf, -np.inf]).any(1)]




    print(tsne_lda_df.describe())
    # find the most probable topic for each news
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

    


    colormap =  np.array([])

    for i  in  range(n_topics):
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        colormap = np.append(colormap, color)




    raw_topic_summaries = []
    for x in _lda_keys:
        raw_topic_summaries.append(topic_summaries[x])

    # plot

    t6 = time.time()
    title = " t-SNE visualization of LDA model trained on {} files, " \
            "{} topics, {} data " \
            "points and top {} words".format(
        X_topics.shape[0], n_topics, num_example, n_top_words)

    plot_lda = bp.figure(plot_width=1200, plot_height=800,
                        title=title,
                        tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                        x_axis_type=None, y_axis_type=None, min_border=1)

    if n_data < 30 :
        dot_size = 20
    if n_data>=30 and n_data<50:
        dot_size = 15
    if n_data>=50 and n_data<150:
        dot_size = 11
    if n_data>=150:
        dot_size = 5


    source = bp.ColumnDataSource(data=dict(x=tsne_lda_df.iloc[:, 0], y=tsne_lda_df.iloc[:, 1], color = colormap[_lda_keys][:num_example], file_names = file_names, raw_topic_summaries = raw_topic_summaries))
    plot_lda.scatter(x='x', y='y',
                    color='color',
                    source=source, size = dot_size)


    plot_lda.outline_line_width = 7
    plot_lda.outline_line_alpha = 0.3
    plot_lda.outline_line_color = "#353A40"

    
    # randomly choose a news (in a topic) coordinate as the crucial words coordinate
    topic_coord = np.empty((X_topics.shape[1], 2)) * np.nan
    for topic_num in _lda_keys:
        if not np.isnan(topic_coord).any():
            break
        topic_coord[topic_num] = tsne_lda[_lda_keys.index(topic_num)]

    # plot crucial words
    for i in range(X_topics.shape[1]):
        plot_lda.text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])
    



    # hover tools
    hover = plot_lda.select(dict(type=HoverTool))
    hover.tooltips = [("file name", "@file_names"), ("topic summary", '@raw_topic_summaries')]

    t7 = time.time()
    print("Time for Bokeh plotting: " + str(t7-t6))

    print ('\n>>> whole process done; took {} mins\n'.format((t7 - t0) / 60.))

    

    html = file_html(plot_lda, CDN)

    raw_topic_summaries_path = "pickles/raw_topic_summaries" + str(myid) + '.p'
    lda_keys_path = "pickles/lda_keys_path" + str(myid) + '.p'

    pickle.dump( raw_topic_summaries, open( raw_topic_summaries_path, "wb" ) )
    pickle.dump( _lda_keys, open( lda_keys_path, "wb" ) )
    

    return html