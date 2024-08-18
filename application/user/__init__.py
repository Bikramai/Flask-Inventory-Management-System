from functools import wraps

from flask import Blueprint, abort
from flask_login import current_user
from application.extension import log_message

# CONFIGURING USER ROUTES
user = Blueprint('user', __name__
                  , url_prefix='/user'
                  , template_folder="./templates"
                  , static_folder="./static")


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin:
            if current_user.is_admin:
                log_message(current_user.username, "Forbidden Access to User")
            abort(403)
        return f(*args, **kwargs)

    return decorated_function

import application.user.product