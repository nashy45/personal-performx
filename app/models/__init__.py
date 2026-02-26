from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.task import Task
from app.models.goal import Goal

__all__ = ['db', 'User', 'Task', 'Goal']
