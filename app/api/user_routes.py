from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User
from app.models import roles_required

user_routes = Blueprint('users', __name__)

@user_routes.route('/')
@login_required
@roles_required('admin')
def users():
    """
    ADMIN: Query for all users and returns them in a list of user dictionaries
    """
    users = User.objects()
    return {'users': [user.to_dict() for user in users]}
