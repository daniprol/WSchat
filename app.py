from flask import Flask, render_template, redirect, url_for
# from wtform_fields import *
import wtform_fields as wtff
from flask_sqlalchemy import SQLAlchemy
from models import User
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
# Secret key to sign the cookies in the flask sessions
# TODO: INCLUDE THIS KEY IN AN ENVIRONMENT VARIABLE
app.secret_key = 'replace later'


# CONFIGURA THE POSGRESQL:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ucwfgmqekuecmj:ad6d850578f0432d47e13830ea6cb2d4acd6305dc2a96c0011433f222580c7f3@ec2-99-81-238-134.eu-west-1.compute.amazonaws.com:5432/d24a6roloe9vos'

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():

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
        return 'Login was successful!'

    # We also return this for GET requests!
    return render_template('login.html', form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
