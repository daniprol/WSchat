from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

# We need to give the form a name to define it:


class RegistrationForm(FlaskForm):
    ''' Registration Form '''

    # 'username_label' refers to the <Label> tag in the HTML
    username = StringField('username_label',
                           validators=[InputRequired(message='Username is required'),
                                       Length(min=4, max=25, message='Username must be between 4 and 25 characters')]
                           )
    # If you want to add a placeholder from here: render_kw={"placeholder": "Username"}

    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password is required'),
                                         Length(min=4, max=25, message='Password must be between 4 and 25 characters')]
                             )
    confirm_password = PasswordField(
        'confirm_password_label', validators=[InputRequired(message='Password is required'), EqualTo('password')])

    submit_button = SubmitField('Create')