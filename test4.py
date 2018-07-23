
from extractor import extract
import os
from compressed_main import stem
from lda_tsne_model import lda_tsne

totalvocab_stemmed = []
totalvocab_tokenized = []
total_text = []
file_names = []

for filename in os.listdir('uploads/small_batch'):
    text, tokens, keywords = extract(os.path.join('uploads/small_batch', filename))
    totalvocab_stemmed.extend(stem(tokens))
    totalvocab_tokenized.extend(tokens)
    total_text.append(text)
    file_names.append(filename)

lda_tsne(total_text, file_names)