from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import User, db, Runs
import datetime

runs_routes = Blueprint('runs', __name__)

def verify_user():
    verified_user = dict(db['user'].find({"email": current_user.email}))
    if (verified_user.__len__() == 0):
        return "error"
    return verified_user

@runs_routes.route('/')
@login_required
def get_user_runs():
    verified_user = verify_user()
    user_runs = {
        'runs': verified_user['runs']
    }
    return user_runs

@runs_routes.route('/<int:id>')
@login_required
def get_user_run_by_id(id):
    verified_user = verify_user()
    temp_list = verified_user['runs']
    for run in temp_list:
        if (run['id'] == id):
            return run
    return "error"

@runs_routes.route('/', methods=['POST'])
@login_required
def create_run():
    verified_user = verify_user()
    req_body = request.json
    new_run = Runs(date=datetime.datetime.now(), duration=req_body["duration"], distance=req_body["distance"])
    update_run = User.objects(email=verified_user['email'])
    update_run.update(add_to_set__runs=[new_run])
    return "success"
