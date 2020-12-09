from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256

# We need to give the form a name to define it:


def invalid_credentials(form, field):
    username_introduced = form.username.data
    # password_introduced = form.password.data
    # In this case field=password:
    password_introduced = field.data

    user_object = User.query.filter_by(username=username_introduced).first()

    if user_object is None:
        raise ValidationError(
            'Username or password is incorrect. Please try again!')
    elif pbkdf2_sha256.verify(password_introduced, user_object.password):
        return
    else:
        raise ValidationError(
            'Username or password is incorrect. Please try again!')


class RegistrationForm(FlaskForm):
    ''' Registration Form '''

    # 'username_label' refers to the <Label> tag in the HTML
    username = StringField('username_label',
                           validators=[
                               InputRequired(message='Username is required'),
                               Length(min=4, max=25, message='Username must be between 4 and 25 characters')]
                           )
    # If you want to add a placeholder from here: render_kw={"placeholder": "Username"}

    password = PasswordField('password_label',
                             validators=[
                                 InputRequired(message='Password is required'),
                                 Length(min=4, max=25, message='Password must be between 4 and 25 characters')]
                             )
    confirm_password = PasswordField(
        'confirm_password_label', validators=[
            InputRequired(message='Password is required'),
            EqualTo('password')])

    submit_button = SubmitField('Create')

    # Create a custom validator:

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        # Note the we need to user username.data

        if user_object:
            raise ValidationError(
                'Username already exists! Select a different one!')


class LoginForm(FlaskForm):
    ''' Login Form '''

    # 'username_label' refers to the <Label> tag in the HTML
    username = StringField('username_label',
                           validators=[
                               InputRequired(message='Username is required')]
                           )
    # If you want to add a placeholder from here: render_kw={"placeholder": "Username"}

    password = PasswordField('password_label',
                             validators=[
                                 InputRequired(message='Password is required'), invalid_credentials]
                             )

    submit_button = SubmitField('Create')

    # Create a custom validator:

    # def validate_username(self, username):
    #     user_object = User.query.filter_by(username=username.data).first()
    #     # Note the we need to user username.data

    #     if not user_object:
    #         raise ValidationError(
    #             'Username or password was incorrect. Please try again!')

    # def validate_password(self, password):
    #     user_object = User.query.filter_by(username=username.data).first()
    #     # Note the we need to user username.data

    #     if not user_object:
    #         raise ValidationError(
    #             'Username or password incorrect. Please, try again!')
    #     elif user_object and user_object.password != password.data:
    #         raise ValidationError(
    #             'Username or password incorrect. Please, try again!')
    #     else:
    #         pass
    # return 'Login was successful!'
