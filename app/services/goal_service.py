"""Goal service for goal-related operations"""
from datetime import datetime
from app.models import db, Goal
from app.utils.validators import calculate_goal_progress

class GoalService:
    """Service class for goal operations"""

    @staticmethod
    def create_goal(title, description, target_date, user_id):
        if not title:
            return None, "Goal title is required"
        try:
            target_datetime = datetime.strptime(target_date, '%Y-%m-%d') if target_date else None
            new_goal = Goal(title=title, description=description,
                            target_date=target_datetime, user_id=user_id)
            db.session.add(new_goal)
            db.session.commit()
            return new_goal, "Goal created successfully"
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD"
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating goal: {str(e)}"

    @staticmethod
    def get_user_goals(user_id):
        return Goal.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_goal(goal_id):
        return Goal.query.get(goal_id)

    @staticmethod
    def update_goal(goal_id, user_id, title, description, target_date):
        """Update an existing goal"""
        goal = Goal.query.get(goal_id)
        if not goal:
            return False, "Goal not found"
        if goal.user_id != user_id:
            return False, "Not authorized"
        if not title:
            return False, "Title is required"
        try:
            goal.title       = title
            goal.description = description
            goal.target_date = datetime.strptime(target_date, '%Y-%m-%d') if target_date else None
            db.session.commit()
            return True, "Goal updated successfully"
        except ValueError:
            return False, "Invalid date format"
        except Exception as e:
            db.session.rollback()
            return False, f"Error updating goal: {str(e)}"

    @staticmethod
    def complete_goal(goal_id, user_id):
        """Toggle goal completion"""
        goal = Goal.query.get(goal_id)
        if not goal:
            return False, "Goal not found"
        if goal.user_id != user_id:
            return False, "Not authorized"
        try:
            goal.completed = not goal.completed
            db.session.commit()
            status = "marked as complete" if goal.completed else "reopened"
            return True, f"Goal {status}"
        except Exception as e:
            db.session.rollback()
            return False, f"Error: {str(e)}"

    @staticmethod
    def delete_goal(goal_id, user_id):
        goal = Goal.query.get(goal_id)
        if not goal:
            return False, "Goal not found"
        if goal.user_id != user_id:
            return False, "Not authorized to delete this goal"
        try:
            db.session.delete(goal)
            db.session.commit()
            return True, "Goal deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting goal: {str(e)}"

    @staticmethod
    def get_goal_progress(goal):
        if goal.completed:
            return 100
        return calculate_goal_progress(goal)
