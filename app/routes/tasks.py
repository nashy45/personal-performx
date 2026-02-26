"""Task routes blueprint"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import TaskService, GoalService

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date    = request.form.get('due_date', '').strip()
        priority    = request.form.get('priority', 'Medium')
        goal_id     = request.form.get('goal_id', type=int) or None
        task, message = TaskService.create_task(title, description, due_date,
                                                current_user.id, goal_id, priority)
        flash(message, 'success' if task else 'danger')
        if task:
            return redirect(url_for('dashboard.index'))
    goals = GoalService.get_user_goals(current_user.id)
    return render_template('add_task.html', goals=goals)

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = TaskService.get_task(task_id)
    if not task or task.user_id != current_user.id:
        flash("Task not found", 'danger')
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date    = request.form.get('due_date', '').strip()
        priority    = request.form.get('priority', 'Medium')
        goal_id     = request.form.get('goal_id', type=int) or None
        success, message = TaskService.update_task(task_id, current_user.id,
                                                   title, description, due_date,
                                                   priority, goal_id)
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('dashboard.index'))
    goals = GoalService.get_user_goals(current_user.id)
    return render_template('edit_task.html', task=task, goals=goals)

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
@login_required
def complete(task_id):
    success, message = TaskService.complete_task(task_id, current_user.id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.index'))

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    success, message = TaskService.delete_task(task_id, current_user.id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.index'))
