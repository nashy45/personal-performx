"""Dashboard routes blueprint"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services import TaskService, GoalService
from datetime import date, datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='')

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Display user dashboard with analytics"""
    tasks = TaskService.get_user_tasks(current_user.id)
    goals = GoalService.get_user_goals(current_user.id)

    # Calculate progress for each goal
    for goal in goals:
        goal.progress = GoalService.get_goal_progress(goal)

    # --- Task Analytics ---
    total_tasks     = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    pending_tasks   = total_tasks - completed_tasks
    today = date.today()
    overdue_tasks   = sum(
        1 for t in tasks
        if not t.completed and t.due_date and t.due_date.date() < today
    )
    completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks else 0)

    # Priority breakdown (pending only)
    high_tasks   = sum(1 for t in tasks if not t.completed and t.priority == 'High')
    medium_tasks = sum(1 for t in tasks if not t.completed and t.priority == 'Medium')
    low_tasks    = sum(1 for t in tasks if not t.completed and t.priority == 'Low')

    # --- Goal Analytics ---
    total_goals = len(goals)
    avg_goal_progress = round(
        sum(g.progress for g in goals) / total_goals if total_goals else 0
    )
    goals_on_track  = sum(1 for g in goals if g.progress >= 50)
    goals_behind    = total_goals - goals_on_track

    # Sort tasks: incomplete first, then by due date (use datetime.max for tasks with no due date)
    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t.completed, t.due_date or datetime.max)
    )

    analytics = {
        'total_tasks':      total_tasks,
        'completed_tasks':  completed_tasks,
        'pending_tasks':    pending_tasks,
        'overdue_tasks':    overdue_tasks,
        'completion_rate':  completion_rate,
        'high_tasks':       high_tasks,
        'medium_tasks':     medium_tasks,
        'low_tasks':        low_tasks,
        'total_goals':      total_goals,
        'avg_goal_progress':avg_goal_progress,
        'goals_on_track':   goals_on_track,
        'goals_behind':     goals_behind,
    }

    return render_template(
        'dashboard.html',
        tasks=sorted_tasks,
        goals=goals,
        analytics=analytics,
        today=today,
    )
