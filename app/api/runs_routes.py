from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import User, db
from app.models.runs import Runs
import datetime
import json

runs_routes = Blueprint('runs', __name__)

@runs_routes.route('/', methods=['GET'])
@login_required
def get_user_runs():
    #verified_user = verify_user()
    # user_runs = {
    #     'runs': verified_user['runs']
    # }
    user_list = User.objects(email=current_user.email)
    return jsonify(user_list[0]["runs"]) #user_runs

@runs_routes.route('/<int:id>')
@login_required
def get_user_run_by_id(id):
    #verified_user = verify_user()
    
    temp = json.loads(User.objects(email=current_user.email).to_json())
    temp_list = temp[0]['runs']
    for run in temp_list:
        if (run['run_id'] == id):
            return run
    return "error"

@runs_routes.route('/', methods=['POST'])
@login_required
def create_run():
    
    req_body = request.json
    new_run = Runs(date=datetime.datetime.now().replace(microsecond=0), duration=req_body["duration"], distance=req_body["distance"])
    add_run = User.objects(email=current_user.email)
    add_run.update(add_to_set__runs=[new_run])
    return "success"
