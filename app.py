import os
from flask import Flask, render_template, url_for, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user


#Instantiate flask app object
app = Flask(__name__)
#Configure flask app database access client access parameters
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+
                                         os.path.abspath(os.path.dirname(__name__))+
                                         '/database.db'
                                        )
app.config['SECRET_KEY'] = 'secrecyismyname'
# Dabase class definition, database instantiation and database connection
class Base(DeclarativeBase):
    """
    Database model class
    """

db = SQLAlchemy(model_class=Base)
db.init_app(app=app)

# Database USER model definition
class User(db.Model, UserMixin):
    """
        Class that defines the database table scheme
        for the user authentication data 
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    """
    Landing page
    
    """
    return render_template('home.html')

