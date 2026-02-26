"""Task service for task-related operations"""
from datetime import datetime
from app.models import db, Task

class TaskService:
    """Service class for task operations"""
    
    @staticmethod
    def create_task(title, description, due_date, user_id, goal_id=None, priority='Medium'):
        """Create a new task"""
        if not title:
            return None, "Task title is required"
        try:
            due_datetime = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
            new_task = Task(title=title, description=description, due_date=due_datetime,
                            user_id=user_id, goal_id=goal_id, priority=priority)
            db.session.add(new_task)
            db.session.commit()
            return new_task, "Task created successfully"
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD"
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating task: {str(e)}"

    @staticmethod
    def get_user_tasks(user_id):
        return Task.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_task(task_id):
        return Task.query.get(task_id)

    @staticmethod
    def update_task(task_id, user_id, title, description, due_date, priority, goal_id=None):
        """Update an existing task"""
        task = Task.query.get(task_id)
        if not task:
            return False, "Task not found"
        if task.user_id != user_id:
            return False, "Not authorized"
        if not title:
            return False, "Title is required"
        try:
            task.title       = title
            task.description = description
            task.priority    = priority
            task.goal_id     = goal_id
            task.due_date    = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
            db.session.commit()
            return True, "Task updated successfully"
        except ValueError:
            return False, "Invalid date format"
        except Exception as e:
            db.session.rollback()
            return False, f"Error updating task: {str(e)}"

    @staticmethod
    def complete_task(task_id, user_id):
        """Mark task as complete"""
        task = Task.query.get(task_id)
        if not task:
            return False, "Task not found"
        if task.user_id != user_id:
            return False, "Not authorized to complete this task"
        try:
            task.completed = True
            db.session.commit()
            return True, "Task marked as complete"
        except Exception as e:
            db.session.rollback()
            return False, f"Error completing task: {str(e)}"

    @staticmethod
    def delete_task(task_id, user_id):
        """Delete a task"""
        task = Task.query.get(task_id)
        if not task:
            return False, "Task not found"
        if task.user_id != user_id:
            return False, "Not authorized to delete this task"
        try:
            db.session.delete(task)
            db.session.commit()
            return True, "Task deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting task: {str(e)}"
