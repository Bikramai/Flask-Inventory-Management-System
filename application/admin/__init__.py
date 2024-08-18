from functools import wraps

from flask import Blueprint, abort
from flask_login import current_user
from application.extension import log_message

# CONFIGURING ADMIN ROUTES
admin = Blueprint('admin', __name__
                  , url_prefix='/admin'
                  , template_folder="admin_templates"
                  , static_folder="static")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            if not current_user.is_admin:
                log_message(current_user.username, "Forbidden Access to Admin")
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


import application.admin.product
import application.admin.users
import application.admin.category
import application.admin.reviews
