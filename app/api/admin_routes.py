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

# user stats (admin)
# @runs_routes.route('/')
# @login_required
# @roles_required('admin')