from flask import Flask, render_template
# from wtform_fields import *
import wtform_fields as wtff
from flask_sqlalchemy import SQLAlchemy
from models import User

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

        # Check that username is not already in the database:
        # user_object = User.query.filter_by(username=username).first()

        # if user_object:
        #     return 'Someone else already has that username!'

        # Create a user:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return 'User added to the database successfully!'
    # else:
    #     return 'Validation error!'

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)
