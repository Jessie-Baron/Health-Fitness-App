from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.objects(email=email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.objects(username=username).first()
    if user:
        raise ValidationError('Username is already in use.')

def check_role(form, field):
    # Checking if valid role
    role = field.data
    if role not in ['user', 'admin']:
        raise ValidationError('Inputted \'role\' is not valid.\t[ROLE]: ' + role)

class AdminSignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), username_exists])
    email = StringField('email', validators=[DataRequired(), user_exists])
    password = StringField('password', validators=[DataRequired()])
    role = StringField('role', validators=[DataRequired(), check_role])