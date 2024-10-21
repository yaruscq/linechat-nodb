from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    """" Registration Form """
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=2, max=25, message="Username must be between 2 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Username must be between 2 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Password must match")])
    submit_button = SubmitField('Create')
