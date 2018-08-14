import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3

from stopwords import stop_word_list


from wordcloud import WordCloud, STOPWORDS






def build_word_cloud(token_list, n):
    words  = token_list
    stop_words = stop_word_list()

   

    

    wordcloud = WordCloud(width=1440, height=1080,
                          background_color='white',
                         #colormap="Blues",
                         #margin=10,
                          stopwords=stop_words,
                          max_words=n,
                         ).generate(str(words))



    fig = plt.figure(figsize=(13, 9))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.margins(x=0, y=0)
    
    html = mpld3.fig_to_html(fig, no_extras=True, template_type='general')

 

    return html




