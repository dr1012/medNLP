import os
import zipfile
from extractor import extract
from stopwords import stop_word_list
from nltk.stem.snowball import SnowballStemmer
import spacy
import rarfile
from flask import session
import flask
from config import Config
myid = Config.myid


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
def decompress(file_path, compressed_file_name):

    compressed_file_name_without_extension = compressed_file_name.split('.')[0]

    main_extension = compressed_file_name.split('.')[1].lower()

    compressed_file_name_without_extension_uuid = compressed_file_name_without_extension + "_" + str(myid)


    if not os.path.exists('uploads/extracted/'+ str(compressed_file_name_without_extension_uuid)):
         os.makedirs('uploads/extracted/'+ str(compressed_file_name_without_extension_uuid))


    if main_extension == 'zip':
    
        zipped = zipfile.ZipFile(file_path, 'r')
        count = 0
        for element in zipped.namelist():
            extension = element.rsplit('.', 1)[1].lower()
            if extension in  ['txt', 'pdf', 'docx']:
                count = count + 1
                zipped.extract(element, 'uploads/extracted/'+ str(compressed_file_name_without_extension_uuid))


        
        zipped.close()

        if count == 0:
            os.rmdir('uploads/extracted/'+ str(compressed_file_name_without_extension_uuid)) 

    elif main_extension == 'rar':
       

        zipped = rarfile.RarFile(file_path, 'r')
        count = 0
        for element in zipped.namelist():
            extension = element.rsplit('.', 1)[1].lower()
            if extension in  ['txt', 'pdf', 'docx']:
                count = count + 1
                zipped.extract(element, 'uploads/extracted/'+ str(compressed_file_name_without_extension_uuid))

        zipped.close()

        if count == 0:
            os.rmdir('uploads/extracted/'+ str(compressed_file_name_without_extension_uuid)) 


    


def handle_compressed_file(file_path,compressed_file_name):
    decompress(file_path, compressed_file_name)

    compressed_file_name_without_extension = compressed_file_name.split('.')[0]

    compressed_file_name_without_extension_uuid = compressed_file_name_without_extension + "_" + str(myid)

    compressed_file_name_uuid = compressed_file_name + "_" + str(myid)

    session['compressed_file_name'] = compressed_file_name
    session['compressed_file_name_without_extension'] = compressed_file_name_without_extension
    session['compressed_file_name_without_extension_uuid'] = compressed_file_name_without_extension_uuid
    session['compressed_file_name_uuid'] = compressed_file_name_uuid
    
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    total_text = []
    file_names = []

    for filename in os.listdir('uploads/extracted/'+ str(compressed_file_name_without_extension_uuid)):
        mypath = 'uploads/extracted/'+ str(compressed_file_name_without_extension_uuid)
        text, tokens, keywords = extract(os.path.join(mypath, filename))
        totalvocab_stemmed.extend(stem(tokens))
        totalvocab_tokenized.extend(tokens)
        total_text.append(text)
        file_names.append(filename)

    return total_text, totalvocab_stemmed, totalvocab_tokenized,  file_names