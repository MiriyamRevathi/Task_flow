"""
RBAC Middleware & Route Decorators.
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, abort
from taskflow.security.session_manager import SessionManager
from taskflow.models.enums import UserRole


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SessionManager.is_authenticated():
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not SessionManager.is_authenticated():
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("auth.login", next=request.url))

            user_role = SessionManager.get_current_role()
            if user_role not in allowed_roles and user_role != UserRole.SUPER_ADMIN.value:
                flash("You do not have permission to perform this action.", "danger")
                return redirect(url_for("auth.unauthorized"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
