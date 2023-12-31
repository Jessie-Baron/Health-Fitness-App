from flask import Blueprint, jsonify, session, request
from app.models import User
from app.forms import LoginForm
from app.forms import SignUpForm
from app.forms import AdminSignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app.models import roles_required
import json

auth_routes = Blueprint('auth', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user:
        print('this is the current user >>>>>>', current_user)
        return current_user.to_dict()
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    req_body = request.json
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        #user = User.query.filter(User.email == form.data['email']).first()
        print("Getting User...")
        user = json.loads(User.objects(email=req_body['email']).to_json())[0]
        checked_user = User(_id=user['_id']['$oid'], username=user['username'], email=user['email'], role=user['role'], hashed_password=['hashed_password'])
        print(user)
        print(checked_user._id)
        login_user(checked_user)
        return user
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            role='user',
            hashed_password=generate_password_hash(form.data['password']),
            runs=list()
        )
        user.save()
        login_user(user)
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401

@auth_routes.route('/admin/signup', methods=['POST'])
@login_required
@roles_required('admin')
def admin_sign_up_user():
    """
    ADMIN: Creates a new user with custom role
    """
    form = AdminSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            role=form.data['role'],
            hashed_password=generate_password_hash(form.data['password']),
            runs=list()
        )
        user.save()
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401
