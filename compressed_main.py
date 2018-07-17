import os
import zipfile
from extractor import extract
from stopwords import stop_word_list
from nltk.stem.snowball import SnowballStemmer
import spacy


nlp = spacy.load('en_core_web_sm')

#http://brandonrose.org/clustering


stemmer = SnowballStemmer("english")

stop_words = stop_word_list()


def stem(tokens):
    stems = [stemmer.stem(t) for t in tokens]
    return stems


#https://www.oreilly.com/learning/how-can-i-tokenize-a-sentence-with-python
def custom_tokenize(text):
    doc = nlp(text)
    special_char = ['#', '<', '>',  '*', '+', ' - ', '~', '^']
    tokens = [token.orth_ for token in doc if not token.orth_.isspace() and not token.is_punct and not token.orth_ in special_char]
    return tokens

def  tokenize_and_stem(text):
    return stem(custom_tokenize(text))






#https://code.tutsplus.com/tutorials/compressing-and-extracting-files-in-python--cms-26816
def decompress(file_path):
    
    zipped = zipfile.ZipFile(file_path, 'r')
    for element in zipped.namelist():
        extension = element.rsplit('.', 1)[1].lower()
        if extension in  ['txt', 'pdf', 'docx']:
            zipped.extract(element, 'uploads/extracted')


    
    zipped.close()


def handle_compressed_file(file_path):
    decompress(file_path)

    
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    total_text = []
    file_names = []

    for filename in os.listdir('uploads/extracted'):
        text, tokens, keywords = extract(os.path.join('uploads/extracted', filename))
        totalvocab_stemmed.extend(stem(tokens))
        totalvocab_tokenized.extend(tokens)
        total_text.append(text)
        file_names.append(filename)

    return total_text, totalvocab_stemmed, totalvocab_tokenized,  file_names


