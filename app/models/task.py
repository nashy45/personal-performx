from app.models import db

class Task(db.Model):
    """Task model for user tasks"""
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(10), default='Medium')
    completed = db.Column(db.Boolean, default=False)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'
