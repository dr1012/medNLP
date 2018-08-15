import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
from stopwords import stop_word_list
from wordcloud import WordCloud, STOPWORDS


def build_word_cloud(token_list, n):
    '''
    Plots the wordcloud from a given token list and returns the plot in html format to be embedded in a html file.

    Parameters
    ----------
    token_list : list
        a list of tokens that will be used to construct the wordcloud. The greater the frequency of a given token, the larger it will appear in the wordcloud.
    n : int:
        maximum number of tokens to display in the wordcloud.

    Returns
    ----------
    Embedded html of the wordcloud visulisation. This can be simply added to a html template.

    '''
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




