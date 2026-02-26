from datetime import datetime, date, timedelta

def validate_email(email):
    """Validate email format"""
    if not email or '@' not in email:
        return False
    return True

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def validate_date_format(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def calculate_goal_progress(goal):
    """
    Calculate goal progress percentage (0-100).
    - If tasks are linked: percentage of completed tasks.
    - Else if target_date set: time elapsed in a 90-day window before target.
    - Otherwise: 0.
    """
    # Task-based (most meaningful)
    if hasattr(goal, 'tasks') and goal.tasks:
        total     = len(goal.tasks)
        completed = sum(1 for t in goal.tasks if t.completed)
        return round((completed / total) * 100) if total else 0

    # Time-based fallback
    if not goal.target_date:
        return 0

    today  = date.today()
    target = goal.target_date.date()

    if today >= target:
        return 100

    # Use a 90-day window ending at the target date
    window_start = target - timedelta(days=90)
    if today <= window_start:
        return 0

    elapsed = (today - window_start).days
    return min(99, round((elapsed / 90) * 100))
