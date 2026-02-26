"""Goal routes blueprint"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import GoalService

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add a new goal"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        target_date = request.form.get('target_date', '').strip()
        
        goal, message = GoalService.create_goal(title, description, target_date, current_user.id)
        
        if goal:
            flash(message, 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash(message, 'danger')
    
    return render_template('add_goal.html')

@goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete(goal_id):
    """Delete a goal"""
    success, message = GoalService.delete_goal(goal_id, current_user.id)
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.index'))
