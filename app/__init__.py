import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from .models import db, User
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.runs_routes import runs_routes
import json


app = Flask(__name__, static_folder='../react-app/build', static_url_path='/')


app.config['MONGODB_SETTINGS'] = {
    'db': 'health_fitness_app',
    'host': 'localhost',
    'port': 27017
}
app.config['SECRET_KEY'] = "flask-is-cool"
# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(email):
    temp = json.loads(User.objects(email=email).to_json())[0]
    temp_user = User(_id=temp['_id']['$oid'], username=temp['username'], email=temp['email'], role=temp['role'], runs=temp['runs'])
    return temp_user


# Tell flask about our seed commands
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(runs_routes, url_prefix='/api/runs')
db.init_app(app)

# Application Security
CORS(app)

@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get(
            'FLASK_ENV') == 'production' else None,
        httponly=True)
    return response


@app.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    route_list = { rule.rule: [[ method for method in rule.methods if method in acceptable_methods ],
                    app.view_functions[rule.endpoint].__doc__ ]
                    for rule in app.url_map.iter_rules() if rule.endpoint != 'static' }
    return route_list


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


def insert_test_data():
    test_users = [
        {
            "username": "test3",
            "email": "test3@email.com",
            "hashed_password": "pbkdf2:sha256:260000$PnCHdPUPWbXcTY2p$b035fc26255f307f6d9f86055f05b38b9bc833f88e113c3cac255413cffa990f",
            "runs": [
                {
                    "run_id": 2,
                    "date": "2023-08-28T13:58:47.217",
                    "duration": "01:20:00",
                    "distance": 13
                }
            ]
        },
        {
            "username": "test4",
            "email": "test4@email.com",
            "hashed_password": "pbkdf2:sha256:260000$PnCHdPUPWbXcTY2p$b035fc26255f307f6d9f86055f05b38b9bc833f88e113c3cac255413cffa990f",
            "runs": [
                {
                    "run_id": 21,
                    "date": "2023-08-29T13:41:42",
                    "duration": "75",
                    "distance": 4.58
                }
            ]
        }
    ]

    user_collection = db.users
    user_collection.insert_many(test_users)

    for user in test_users:
        user.save()

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
