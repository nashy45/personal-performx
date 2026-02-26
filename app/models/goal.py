from app.models import db

class Goal(db.Model):
    """Goal model for user goals"""
    __tablename__ = 'goal'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='goal', lazy=True)
    
    def __repr__(self):
        return f'<Goal {self.title}>'
