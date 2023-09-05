from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


<<<<<<< HEAD
# def user_exists(form, field):
#     # Checking if user exists
#     email = field.data
#     user = User.query.filter(User.email == email).first()
#     if user:
#         raise ValidationError('Email address is already in use.')


# def username_exists(form, field):
#     # Checking if username is already in use
#     username = field.data
#     user = User.query.filter(User.username == username).first()
#     if user:
#         raise ValidationError('Username is already in use.')
=======
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
>>>>>>> 6e39b79cdaffe2453e20b2c592fa04ae0264a63a


class SignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
