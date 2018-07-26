from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')



class UploadFileForm(FlaskForm):
    document = FileField('document', validators = [FileRequired])
    submit = SubmitField('Upload')


class inputText(FlaskForm):
    text = TextAreaField('input_text', validators = [DataRequired])
    submit = SubmitField('Submit')

class inputTopicNumber(FlaskForm):
    number_topics = IntegerField('number_topics', render_kw={"placeholder": "New number of topics"})
    number_topwords = IntegerField('number_topwords', render_kw={"placeholder": "New number of top words"})
    threshold = FloatField('threshold', render_kw={"placeholder": "New topic probability threshold"})
    submit = SubmitField('Submit')