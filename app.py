from flask import Flask, render_template, redirect, url_for, flash
# from wtform_fields import *
import wtform_fields as wtff
from flask_sqlalchemy import SQLAlchemy
from models import User
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

import os
from dotenv import load_dotenv
load_dotenv()

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
# Secret key to sign the cookies in the flask sessions
# TODO: INCLUDE THIS KEY IN AN ENVIRONMENT VARIABLE
app.secret_key = 'replace later'


# CONFIGURA THE POSGRESQL:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(app)

# Configure flask login:
# TODO: check if we need to pass the app as an argument here!
login = LoginManager(app)
login.init_app(app)

# Create the function to load a /user from the id:


@login.user_loader
def load_user(id):
    # User.query.filter_by(id=id).first()
    # We are storing id's as integers in the db!
    # We don't need to use the .first() method because ids are unique
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    print(current_user)
    # Instantiate the form:
    reg_form = wtff.RegistrationForm()

    # We need to trigger the validators for the form:
    # This will return True if the validation was correct
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # We need to generate a hash from the plain text password
        hashed_password = pbkdf2_sha256.hash(password)
        # This modules takes care of the salt and the number of iterations (29000 by default!)
        # If we want to do it manually:
        # pbkdf2_sha256.using(rounds=1000, salt_size=8).hash(password)

        # Check that username is not already in the database:
        # user_object = User.query.filter_by(username=username).first()

        # if user_object:
        #     return 'Someone else already has that username!'

        # Create a user:
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Flash message for succesful registration:
        flash(
            f'Congratulations {username}, your are now a member of our beloved community!')

        return redirect(url_for('login'))
    # else:
    #     return 'Validation error!'

    return render_template('index.html', form=reg_form)


@app.route('/login/', methods=['GET', 'POST'])
def login():

    login_form = wtff.LoginForm()

    if login_form.validate_on_submit():
        # user_object = User.query.filter_by(
        #     username=login_form.username.data).first()
        # # IMPORTANT: you need to call .first() or .all() after the query, otherwise you will receive an object that passes the if statement!

        # if not user_object:
        #     return 'Username or password incorrect. Please, try again!'
        # elif user_object and user_object.password != login_form.password.data:
        #     return 'Username or password incorrect. Please, try again!'
        # else:

        # TODO: we are doing 2 queries for each login (1 for validation and 1 here). This inefficiency should be removed
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)

        print(current_user.get_id())
        # How do we know for sure that the user is logged in? User 'current_user'
        if current_user.is_authenticated:
            flash(f'You are now logged in {user_object.username}!')
            # print(current_user.__dict__)
            return redirect(url_for('index'))
            # return 'Login was successful!'
        else:
            flash('There was a problem in the login process. Please try again!')

    # We also return this for GET requests!
    return render_template('login.html', form=login_form)


@app.route('/chat/', methods=['GET', 'POST'])
@login_required
def chat():
    print(current_user)
    return 'You have accessed a protected route!'


@app.route('/logout/', methods=['GET'])
def logout():
    print(current_user)
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
