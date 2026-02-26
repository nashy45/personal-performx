from functools import wraps
from flask import redirect, url_for, flash, current_app
from flask_login import current_user

def login_required_custom(f):
    """Custom login required decorator with better error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(model_attr='user_id'):
    """Decorator to check if user owns the resource"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in.", "warning")
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
