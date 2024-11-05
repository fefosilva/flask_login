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

#Instantiate Bcrypt object over flask app
bcrypt = Bcrypt(app = app)

#Instantiate LoginManager object
login_manager = LoginManager(app=app)
login_manager.init_app(app=app)
login_manager.login_view = "login"

#Callback function to reload user from active session
@login_manager.user_loader
def load_user(user_id):
    """
        callback function to reload user id from active session
    """
    return User.query.get(int(user_id))


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

# Registration class object definition
class RegisterForm(FlaskForm):
    """
        Register form object class definition
    """
    #username validation parameters
    username = StringField(
        validators=[InputRequired(),Length(min=4,max=20)],
        render_kw={"placeholder": "Username"}
        )
    #password validation parameters
    password = PasswordField(
        validators=[InputRequired(),Length(min=4,max=20)],
        render_kw={"placeholder": "Password"}
        )
    #submit field definition
    submit = SubmitField(label="Register")

    def validate_username(self, username):
        """
            Username validation function
        """
        existing_username = User.query.filter_by(username = username.data).first()

        if existing_username:
            raise ValidationError("Username already exist! Please choose another.")

# Login form class object definition
class LoginForm(FlaskForm):
    """
        Login form object class definition
    """
    #username validation parameters
    username = StringField(
        validators=[InputRequired(),Length(min=4,max=20)],
        render_kw={"placeholder": "Username"}
        )

    #password validation parameters
    password = PasswordField(
        validators=[InputRequired(),Length(min=4,max=20)],
        render_kw={"placeholder": "Password"}
        )

    #submit field definition
    submit = SubmitField(label="Login")


@app.route('/')
def home():
    """
    Landing page
    
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Login page
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
        Renders dashboard
    """
    return render_template('dashboard.html')


@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    """
        Logsout user
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
       Sign up page 
    """
    form  = RegisterForm()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_passwd)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
