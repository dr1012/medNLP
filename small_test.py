from lda_tsne_model2 import lda_tsne
import time
import os
from compressed_main import stem
from compressed_main import tokenize_and_stem
from extractor import extract


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



script, div, html = lda_tsne(total_text, file_names, n_topics = 20)



Html_file= open("pyLDAvis_test.html","w")
Html_file.write(html)
Html_file.close()

#pyLDAvis.show(prepared_data)
