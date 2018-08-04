from flask import render_template, Flask, flash, redirect, request, url_for, send_from_directory, make_response, session
import uuid
from flask_session import Session
myid =  str(uuid.uuid4())

from config import Config
import flask

from werkzeug.utils import secure_filename
import os
from extractor import extract, simple_parse
from frequency_distribution import frequency_dist
from mywordcloud import build_word_cloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import urllib.parse
import time
from lda_tsne_model2 import lda_tsne
from compressed_main import handle_compressed_file

import json
import pickle
from mypyldavis import pyladvis_run
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_socketio import SocketIO, emit
import shutil

#gevent
#flask-login
#flask_sqlalchemy
#flask_socketio
#flask-session
#pickle

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'A_g_reat-fuck_ing-secret'

db = SQLAlchemy(app)
socketio = SocketIO(app)

# at initialization, write code that creates uplaods/pickles folders


from models import User, Single_Upload, Group_Upload
from forms import LoginForm, UploadFileForm, inputText, inputTopicNumber, StopWordsForm, RegisterForm, EditAccountForm


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'zip','rar', 'docx'])

compressed_extensions = ['zip', 'rar']


app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

login_settings = LoginManager(app)

login_settings.login_view = 'login_form'

db.create_all()


@socketio.on('disconnect')
def disconnect_user():
    print('DISCONNECT')


@socketio.on('connect')
def connect_user():
    print('CONNECT')

   





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#https://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    uploads_path = 'uploads'
    pickles_path = 'pickles'
    for i in os.listdir(uploads_path):
        if os.path.isfile(os.path.join(uploads_path,i)) and str(myid) in i:
            os.remove()

    for i in os.listdir(pickles_path):
        if os.path.isfile(os.path.join(pickles_path,i)) and str(myid) in i:
            os.remove()



    if request.method == 'POST':
        # check if the post request has the file part
        if 'document' not in request.files:
            print("file not in request.files")
            flash('No file part')
            return redirect(request.url)
        file = request.files['document']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)

            file_extension =  filename.rsplit('.', 1)[1].lower()

            file_name_no_extension = filename.rsplit('.', 1)[0].lower()

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            file_name_uuid = str(file_name_no_extension) + '_' +  str(myid) + '.' + file_extension
            # saved as 'filename_<uuid>.txt
            file.save(os.path.join('uploads', file_name_uuid))

            if file_extension in compressed_extensions:
                total_text, totalvocab_stemmed, totalvocab_tokenized, file_names = handle_compressed_file((os.path.join('uploads', file_name_uuid)), filename)

                if not os.path.exists('pickles'):
                    os.makedirs('pickles')
                
                total_text_path = 'pickles/total_text_'+ str(myid) + '.p'
                file_names_path = 'pickles/file_names_'+ str(myid) + '.p'
                pickle.dump( total_text, open( total_text_path, "wb" ) )
                pickle.dump( file_names, open( file_names_path, "wb" ) )
                

               
                if len(file_names)<4:
                    flash('At least 4 files in the compressed folder are required')
                    return redirect(url_for('upload_file'))
                lda_html = lda_tsne(total_text, file_names)
                topic_number_form = inputTopicNumber()

                
                lda_model_path = "pickles/lda_model_" + str(myid) + '.p'
                document_term_matrix_path = "pickles/document_term_matrix_" + str(myid) + '.p'
                cvectorizer_path = "pickles/cvectorizer_" + str(myid) + '.p'


                pyladvis_html = pyladvis_run(lda_model_path, document_term_matrix_path, cvectorizer_path)

                pyladvis_html_path = "pickles/pyladvis_html_"  + str(myid) + '.p'

                pickle.dump( pyladvis_html, open( pyladvis_html_path, "wb" ) )

                
                


                return render_template('bulk_analysis.html', title = 'Clustering analysis', lda_html = lda_html, number_form = topic_number_form, pyladvis_html = pyladvis_html )
            
            text, tokens, keywords = extract(os.path.join('uploads', file_name_uuid))


            keywords_path = "pickles/keywords_" + str(myid) + '.p'

            pickle.dump( keywords, open( keywords_path, "wb" ) )

            graph_data = frequency_dist(keywords, 26, ('Word frequency for file  with filename: ' + filename))

          

            wordcloud_html = build_word_cloud(text, 2000)

            wordcloud_html_path = "pickles/wordcloud_html_" + str(myid) + '.p'

            pickle.dump(wordcloud_html, open( wordcloud_html_path, "wb" ) )

            

            stop_words_form = StopWordsForm()


            session['title'] = 'Single file NLP analysis'
      
            
            return render_template('analysis_options.html', title='Single file NLP analysis', graph_data = graph_data, wordcloud_html = wordcloud_html,  stop_words_form = stop_words_form)
        
   
        else:
            flash('not an allowed file format')
            return redirect(url_for('upload_file'))
    else:
        uploadForm = UploadFileForm()
        inputTextForm = inputText()
        return render_template('home.html',title = 'Welcome', form = uploadForm, textform = inputTextForm)





@app.route('/submit', methods=['POST'])
def submit():
     if request.method == 'POST':
       
        if 'text' not in request.form:
            print("no text entered")
            flash('No text was entered')
            return redirect(request.url)

        text = request.form['text']
   
        text, tokens, keywords = simple_parse(text)

        keywords_path = "pickles/keywords_" + str(myid) + '.p'

        pickle.dump( keywords, open( keywords_path, "wb" ) )
         
        graph_data = frequency_dist(keywords, 26, ('Word frequency for input text'))

        wordcloud_html = build_word_cloud(text, 2000)

        wordcloud_html_path = "pickles/wordcloud_html_" + str(myid) + '.p'

        pickle.dump(wordcloud_html, open( wordcloud_html_path, "wb" ) )


        session['title'] = 'NLP analysis'
        

        stop_words_form = StopWordsForm()
    
        return render_template('analysis_options.html', title='NLP analysis', graph_data = graph_data, wordcloud_html = wordcloud_html,  stop_words_form = stop_words_form)

#https://stackoverflow.com/questions/47368054/wtforms-test-whether-field-is-filled-out
def is_filled(data):
   if data == None:
      return False
   if data == '':
      return False
   if data == []:
      return False
   return True


@app.route('/submit_number_topics', methods=['POST'])
def submit_number_topics():
    if request.method == 'POST':
        if is_filled(request.form['number_topics']):
            number_topics = int(request.form['number_topics']) 
            session['number_topics'] = str(number_topics)

        else:
            number_topics = int(session['number_topics'])

        if is_filled(request.form['number_topwords']):
            number_topwords = int(request.form['number_topwords'])
            session['number_topwords'] = str(number_topwords)
        
        else:
            number_topwords = int(session['number_topwords'])


        total_text_path = 'pickles/total_text_'+ str(myid) + '.p'
        file_names_path = 'pickles/file_names_'+ str(myid) + '.p'
        pyladvis_html_path = "pickles/pyladvis_html_"  + str(myid) + '.p'

        print()
        print("Paths: ")

        print(total_text_path)
        print(file_names_path)
        print(pyladvis_html_path)

        print()


        total_text = pickle.load( open(total_text_path, "rb" ) )
        file_names = pickle.load(open(file_names_path, "rb" ) )



        pyladvis_html = pickle.load(open(pyladvis_html_path, "rb" ) )
        lda_html = lda_tsne(total_text, file_names, n_topics= number_topics, n_top_words = number_topwords)
        topic_number_form = inputTopicNumber()
        return render_template('bulk_analysis.html', title = 'Clustering analysis',lda_html = lda_html, number_form = topic_number_form, pyladvis_html = pyladvis_html )


@app.route('/submit_stop_words', methods=['POST'])
def submit_stop_words():
    if request.method == 'POST':
        if is_filled(request.form['stopwords']):
            new_stopwords  = request.form['stopwords']
            new_stopwords = new_stopwords.replace(' ','')
            new_stopwords = new_stopwords.split(",")

            keywords_path = "pickles/keywords_" + str(myid) + '.p'

            keywords = pickle.load(open(keywords_path, "rb" ) )
            title = session['title']
            graph_data = frequency_dist(keywords, 26, title, new_stopwords)

            wordcloud_html_path = "pickles/wordcloud_html_" + str(myid) + '.p'

            wordcloud_html = pickle.load(open(wordcloud_html_path, "rb" ) )

            stop_words_form = StopWordsForm()
            return render_template('analysis_options.html', title='Single file NLP analysis', graph_data = graph_data, stop_words_form = stop_words_form, wordcloud_html = wordcloud_html)









##    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins ####



@login_settings.user_loader
def load_user(id):
    return User.query.get(int(id))


## !!!!!!!!this handles both the login template before anyone is logged in and the form submission of the login procress. No need to have two seraprate functions. !!!!!!!!

#If the username and password are both correct, then I call the login_user() function, which comes from Flask-Login. 
# This function will register the user as logged in, so that means that any future pages the user navigates to will have the current_user variable set to that user.
@app.route('/login_form', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload_file'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('upload_file'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('upload_file'))




@app.route('/register_form', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('upload_file'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Submit', form=form)




@app.route('/my_account',  methods=['GET', 'POST'])
@login_required
def my_account():

    def set_password(password):
        return generate_password_hash(password)


    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password_hash = set_password(form.new_password.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('my_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('my_account.html', title='Edit Profile',
                           form=form)


#def delete_files(myid):




if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app)