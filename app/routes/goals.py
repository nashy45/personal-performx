"""Goal routes blueprint"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import GoalService

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        target_date = request.form.get('target_date', '').strip()
        goal, message = GoalService.create_goal(title, description, target_date, current_user.id)
        flash(message, 'success' if goal else 'danger')
        if goal:
            return redirect(url_for('dashboard.index'))
    return render_template('add_goal.html')

@goals_bp.route('/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(goal_id):
    goal = GoalService.get_goal(goal_id)
    if not goal or goal.user_id != current_user.id:
        flash("Goal not found", 'danger')
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        target_date = request.form.get('target_date', '').strip()
        success, message = GoalService.update_goal(goal_id, current_user.id,
                                                   title, description, target_date)
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('dashboard.index'))
    return render_template('edit_goal.html', goal=goal)

@goals_bp.route('/<int:goal_id>/complete', methods=['POST'])
@login_required
def complete(goal_id):
    success, message = GoalService.complete_goal(goal_id, current_user.id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.index'))

@goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete(goal_id):
    success, message = GoalService.delete_goal(goal_id, current_user.id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.index'))
