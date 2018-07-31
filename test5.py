import os
from extractor import extract 
from compressed_main import stem
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
import re
import nltk
import io
import base64
from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
from stopwords import stop_word_list

import time

from wordcloud import WordCloud, STOPWORDS





text = 'The octopus (/ˈɒktəpəs/ or ~/pʊs/) is a soft-bodied, eight-armed mollusc of the order Octopoda. Around 300 species are recognised and the order is grouped within the class Cephalopoda with squids, cuttlefish and nautiloids. Like other cephalopods, the octopus is bilaterally symmetric with two eyes and a beak, with its mouth at the centre point of the arms (which are sometimes mistakenly called "tentacles"). The soft body can rapidly alter its shape, enabling octopuses to squeeze through small gaps. They trail their eight arms behind them as they swim. The siphon is used both for respiration and for locomotion, by expelling a jet of water. Octopuses have a complex nervous system and excellent sight, and are among the most intelligent and behaviourally diverse of all invertebrates. Octopuses inhabit various regions of the ocean, including coral reefs, pelagic waters, and the seabed; some live in the intertidal zone and others at abyssal depths. Most species grow fast, mature early and are short-lived. During breeding, the male uses a specially adapted arm to deliver a bundle of sperm directly into the female\'s mantle cavity, after which he becomes senescent and dies. The female deposits fertilised eggs in a den and cares for them until they hatch, after which she also dies. Strategies to defend themselves against predators include the expulsion of ink, the use of camouflage and threat displays, their ability to jet quickly through the water, and their ability to hide. All octopuses are venomous, but only the blue-ringed octopuses are known to be deadly to humans. Octopuses appear in mythology as sea monsters like the Kraken of Norway and the Akkorokamui of the Ainu, and probably the Gorgon of ancient Greece. A battle with an octopus appears in Victor Hugo\'s book Toilers of the Sea, inspiring other works such as Ian Fleming\'s Octopussy. Octopuses appear in Japanese erotic art, shunga. They are eaten by humans in many parts of the world, especially the Mediterranean and the Asian seas'

n = 2000
words  = text
stop_words = stop_word_list()





wordcloud = WordCloud(width=1440, height=1080,
                        background_color='white',
                        #colormap="Blues",
                        #margin=10,
                        stopwords=stop_words,
                        max_words=n,
                        ).generate(str(words))



fig = plt.figure(figsize=(20, 15))
plt.imshow(wordcloud)
plt.axis('off')
plt.margins(x=0, y=0)
html = mpld3.fig_to_html(fig)

Html_file= open("wordcloud_html","w")
Html_file.write(html)
Html_file.close()




