from .db import db
from mongoengine import *
from .runs import Runs
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(Document, UserMixin):
    __tablename__ = 'users'

    _id = StringField()
    username = StringField()
    email = EmailField(unique=True)
    hashed_password = StringField()
    role = StringField()
    runs = ListField(EmbeddedDocumentField(Runs))

    @property
    def get_id(self):
        return lambda: self.email

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'runs': self.runs
        }
