"""Profile / settings routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import UserService

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            full_name = request.form.get('full_name', '').strip()
            success, message = UserService.update_profile(current_user.id, full_name)
            flash(message, 'success' if success else 'danger')

        elif action == 'change_password':
            current_pw  = request.form.get('current_password', '')
            new_pw      = request.form.get('new_password', '')
            confirm_pw  = request.form.get('confirm_password', '')
            success, message = UserService.change_password(
                current_user.id, current_pw, new_pw, confirm_pw)
            flash(message, 'success' if success else 'danger')

        return redirect(url_for('profile.index'))

    return render_template('profile.html')
