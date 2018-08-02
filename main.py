from flask import render_template, Flask, flash, redirect, request, url_for, send_from_directory, make_response
from config import Config

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
from flask import session
import json
import pickle
from mypyldavis import pyladvis_run
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_socketio import SocketIO, emit

#gevent
#flask-login
#flask_sqlalchemy
#flask_socketio
#pickle




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio = SocketIO(app)

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
    print('DETECTED')
    logout_user()
    #session.clear()





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
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

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            file.save(os.path.join('uploads', filename))

            if file_extension in compressed_extensions:
                total_text, totalvocab_stemmed, totalvocab_tokenized, file_names = handle_compressed_file((os.path.join('uploads', filename)), filename)

                if not os.path.exists('pickles'):
                    os.makedirs('pickles')
                
                pickle.dump( total_text, open( "pickles/total_text.p", "wb" ) )
                pickle.dump( file_names, open( "pickles/file_names.p", "wb" ) )
                

               
                if len(file_names)<4:
                    flash('At least 4 files in the compressed folder are required')
                    return redirect(url_for('upload_file'))
                lda_html = lda_tsne(total_text, file_names)
                topic_number_form = inputTopicNumber()

                
                lda_model_path = "pickles/lda_model.p"
                document_term_matrix_path = "pickles/document_term_matrix.p"
                cvectorizer_path = "pickles/cvectorizer.p"


                pyladvis_html = pyladvis_run(lda_model_path, document_term_matrix_path, cvectorizer_path)

                pickle.dump( pyladvis_html, open( "pickles/pyladvis_html.p", "wb" ) )



                return render_template('bulk_analysis.html', title = 'Clustering analysis', lda_html = lda_html, number_form = topic_number_form, pyladvis_html = pyladvis_html )
            
            text, tokens, keywords = extract(os.path.join('uploads', filename))

            pickle.dump( keywords, open( "pickles/keywords.p", "wb" ) )

            graph_data = frequency_dist(keywords, 26, ('Word frequency for file  with filename: ' + filename))

          

            wordcloud_html = build_word_cloud(text, 2000)

            

            pickle.dump(wordcloud_html, open( "pickles/wordcloud_html.p", "wb" ) )

            

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

        pickle.dump( keywords, open( "pickles/keywords.p", "wb" ) )
         
        graph_data = frequency_dist(keywords, 26, ('Word frequency for input text'))

   

        wordcloud_html = build_word_cloud(text, 2000)


        pickle.dump(wordcloud_html, open( "pickles/wordcloud_html.p", "wb" ) )


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


        total_text = pickle.load( open("pickles/total_text.p", "rb" ) )
        file_names = pickle.load(open("pickles/file_names.p", "rb" ) )

        pyladvis_html = pickle.load(open("pickles/pyladvis_html.p", "rb" ) )
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
            keywords = pickle.load(open("pickles/keywords.p", "rb" ) )
            title = session['title']
            graph_data = frequency_dist(keywords, 26, title, new_stopwords)

            wordcloud_html = pickle.load(open("pickles/wordcloud_html.p", "rb" ) )

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






if __name__ == '__main__':
  app.run(debug=True)