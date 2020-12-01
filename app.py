from flask import Flask, render_template
# from wtform_fields import *
import wtform_fields as wtff

app = Flask(__name__)
# Secret key to sign the cookies in the flask sessions
# TODO: INCLUDE THIS KEY IN AN ENVIRONMENT VARIABLE
app.secret_key = 'replace later'


@app.route('/', methods=['GET', 'POST'])
def index():

    # Instantiate the form:
    reg_form = wtff.RegistrationForm()

    # We need to trigger the validators for the form:
    # This will return True if the validation was correct
    if reg_form.validate_on_submit():
        return 'Success in the form!'
    # else:
    #     return 'Validation error!'

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)
