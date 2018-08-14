import os
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# __file__ is the pathway from which the module was laoded
basedir = os.path.abspath(os.path.dirname(__file__))




class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A_g_reat-fuck_ing-secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    

    





