from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import User, db
from app.models.runs import Runs
import datetime
import json

runs_routes = Blueprint('runs', __name__)

def verify_user():
    verified_user = dict(db['user'].find({"email": current_user.email}))
    if (verified_user.__len__() == 0):
        return "error"
    return verified_user

@runs_routes.route('/', methods=['GET'])
def get_user_runs():
    #verified_user = verify_user()
    # user_runs = {
    #     'runs': verified_user['runs']
    # }
    user_list = User.objects()
    return jsonify(user_list[0]["runs"]) #user_runs

@runs_routes.route('/<int:id>')
def get_user_run_by_id(id):
    #verified_user = verify_user()
    cur_user ={
        'email': 'test@email.com'
    }
    temp = json.loads(User.objects(email=cur_user['email']).to_json())
    temp_list = temp[0]['runs']
    for run in temp_list:
        if (run['run_id'] == id):
            return run
    return "error"

@runs_routes.route('/', methods=['POST'])
def create_run():
    #verified_user = verify_user()
    cur_user ={
        'email': 'test@email.com'
    }
    req_body = request.json
    new_run = Runs(date=datetime.datetime.now().replace(microsecond=0), duration=req_body["duration"], distance=req_body["distance"])
    add_run = User.objects(email=cur_user['email'])
    add_run.update(add_to_set__runs=[new_run])
    return "success"
