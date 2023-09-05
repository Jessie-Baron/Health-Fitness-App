from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import User
from app.models import Runs
import datetime
import json
from app.models import roles_required

runs_routes = Blueprint('runs', __name__)

@runs_routes.route('/', methods=['GET'])
def get_user_runs():
    """
    Query for all of user's runs and returns them in a list of run dictionaries
    """
    user_list = User.objects(email=current_user.email)
    return jsonify(user_list[0]["runs"]) #user_runs

@runs_routes.route('/<int:id>')
def get_user_run_by_id(id):
    """
    Query for one of user's runs by id and returns a run dictionary
    """
    temp = json.loads(User.objects(email=current_user.email).to_json())
    temp_list = temp[0]['runs']
    for run in temp_list:
        if (run['run_id'] == id):
            return run

    error_msg = "Run of id:=" + id + " was not found."
    return {'message': "An error occured", 'status': error_msg}, 404

@runs_routes.route('/', methods=['POST'])
def create_run():
    """
    Query to create run for user and returns success message
    """
    req_body = request.json
    new_run = Runs(date=str(datetime.datetime.now().replace(microsecond=0)).replace(" ", "T"), duration=req_body["duration"], distance=req_body["distance"])
    add_run = User.objects(email=current_user.email)
    add_run.update(add_to_set__runs=[new_run])
    return {'message': "Run successfully created."}, 201

@runs_routes.route('/<int:id>', methods=['PUT'])
def update_run(id):
    """
    Query to update a user run by run_id
    """
    temp = json.loads(User.objects(email=current_user.email).to_json())
    req_body = request.json
    temp_list = temp[0]['runs']
    for run in temp_list:
        if (run['run_id'] == id):
            run['distance'] = req_body['distance']
            run['duration'] = req_body['duration']
            run['date'] = req_body['date']

            update_user = User.objects(email=current_user.email)
            update_user.update(set__runs=temp_list)
            return {'message': "Run successfully updated."}, 200

    error_msg = "Run of id:=" + id + " was not found."
    return {'message': "An error occured", 'status': error_msg}, 404

@runs_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_run(id):
    """
    Query to remove a user run by run_id
    """
    temp = json.loads(User.objects(email=current_user.email).to_json())
    temp_list = temp[0]['runs']
    for run in temp_list:
        if (run['run_id'] == id):
            temp_list.remove(run)

            update_user = User.objects(email=current_user.email)
            update_user.update(set__runs=temp_list)
            return {'message': "Run successfully removed."}, 200

    error_msg = "Run of id:=" + id + " was not found."
    return {'message': "An error occured", 'status': error_msg}, 404

@runs_routes.route('/', methods=['DELETE'])
@login_required
def delete_all_run(id):
    """
    Query to remove all user runs
    """
    update_user = User.objects(email=current_user.email)
    update_user.update(set__runs=list())
    return {'message':"All runs deleted"}, 200
