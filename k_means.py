#http://brandonrose.org/clustering


from compressed_main import tokenize_and_stem
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import random
from sklearn.metrics import silhouette_score

def k_means_model(total_text, totalvocab_stemmed, totalvocab_tokenized,  file_names, n):


    #################################################################################################
    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
    print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    #################################################################################################



    #define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                    min_df=1, stop_words='english',
                                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(total_text) #fit the vectorizer to synopses

    #all the different n-grams in the texts
    terms = tfidf_vectorizer.get_feature_names()

    dist = 1 - cosine_similarity(tfidf_matrix)




    ###########  K means  ####################
    
    num_clusters = n
    
    for n_clusters in range_n_clusters:

    km = KMeans(n_clusters=num_clusters)

    km.fit(tfidf_matrix)

    clusters = km.labels_.tolist()

    print("clusters : ")
    print(clusters)

    files = { 'filename': file_names, 'texts': total_text, 'cluster': clusters}

    frame = pd.DataFrame(files, index =[clusters], columns =['filename', 'cluster'])

    #########  fancy code to find the top few words closest to cluster centroid. Good representation of topic  #############

    print("Top terms per cluster:")
    print()

    #sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

    print("order_centroids:   ")
    print(order_centroids)

    cluster_summaries = []

    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')
        cluster_summary = ""
        for ind in order_centroids[i, :10]: #replace 6 with n words per cluster
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=',')
            cluster_summary = cluster_summary + vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0] + ", "
            
        print() #add whitespace
        print() #add whitespace
        cluster_summaries.append(cluster_summary)
        print("Cluster %d filename:" % i, end='')
        for filename in frame.ix[i]['filename'].values.tolist():
            print(' %s,' % filename, end='')
        print() #add whitespace
        print() #add whitespace

    ##################################################################



    # convert two components as we're plotting points in a two-dimensional plane
    # "precomputed" because we provide a distance matrix
    # we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]


    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#000000',  6: '#FFFF00', 7: '#7EFF33', 8: '#FF33F8', 9: '#334EFF'}


    cluster_names = {}

    for i in range(num_clusters):
        #https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
        color = "%06x" % random.randint(0, 0xFFFFFF)
        cluster_colors.update({i: color})
        cluster_names.update({i: cluster_summaries[i]})

    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, filename=file_names)) 
    groups = df.groupby('label')


    # set up plot
    fig, ax = plt.subplots(figsize=(17, 9)) # set size
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling



    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                label=cluster_names[name], color=cluster_colors[name], 
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom= False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False)
        ax.tick_params(\
            axis= 'y',         # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            left=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelleft=False)
        
    ax.legend(numpoints=1)  #show legend with only 1 point

    #add label in x,y position with the label as the film title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['filename'], size=8)  

    print(cluster_summaries)
        
        
    plt.show()







