from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if not current_user.is_authenticated:
                return {'errors': "User is not logged in."}, 401
            
            if not current_user.role in role_names:
                return {'errors': "User does not have permission for this endpoint."}, 403
            else:
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator