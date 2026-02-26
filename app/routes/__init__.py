"""Initialize routes package"""
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.routes.goals import goals_bp
from app.routes.dashboard import dashboard_bp
from app.routes.profile import profile_bp

__all__ = ['auth_bp', 'tasks_bp', 'goals_bp', 'dashboard_bp', 'profile_bp']
