
####    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
from main import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Single_Upload(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64))
    date_created = db.Column(db.TIMESTAMP())
    text_path = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<File Name {}>'.format(self.file_name)


class Group_Upload(db.Model):
    upload_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64))
    date_created = db.Column(db.TIMESTAMP())
    total_text_path = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vectorizer_path = db.Column(db.String(256))
    dtm_path = db.Column(db.String(256))
    file_names_path = db.Column(db.String(256))
    lda_model_path = db.Column(db.String(256))
    lda_html_path =  db.Column(db.String(256))
    pyldavis_html_path =  db.Column(db.String(256))

    def __repr__(self):
        return '<File Name {}>'.format(self.file_name)
