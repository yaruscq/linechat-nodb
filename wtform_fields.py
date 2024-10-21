from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256

def invalid_credentials(form, field):
    """ Username and password checker """

    username_entered = form.username.data
    password_entered = field.data

    # Check usernane is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None: # type: ignore
        raise ValidationError("Username or password is incorrect.")
    # elif password_entered != user_object.password: # type: ignore
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect.")



class RegistrationForm(FlaskForm):
    """" Registration Form """
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=2, max=25, message="Username must be between 2 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Username must be between 2 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username is already taken. Please choose a different username!")



class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')