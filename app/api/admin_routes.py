from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import User
from app.models import Runs
import datetime
import json
from app.models import roles_required

admin_routes = Blueprint('admin', __name__)

# TODO
# user stats
# user lifttime distance
# 

@admin_routes.route("/user/distance")
@login_required
@roles_required('admin')
def user_total_distance():
    pipeline = [
        {"$match" : {"role": "user"}},
        {"$unwind": "$runs"},
        {"$group" : {
            "_id": "$email",
            "total_distance": {"$sum": {"$cond": [{"$gt":[{"$size": "$runs"}, 0]}, "$runs.distance", 0]}}}
        }
    ]
    user_distances = User.objects().aggregate(pipeline)
    data_print = {
        'data': []
    }
    for x in user_distances:
        data_print['data'].append(x)
        print(x)
    
    return data_print
# user stats (admin)
# @runs_routes.route('/')
# @login_required
# @roles_required('admin')