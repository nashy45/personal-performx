"""Entry point for the Flask application"""
import os
from app import create_app, db
from app.models import User, Task, Goal

# Create app
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """Make database models available in shell context"""
    return {'db': db, 'User': User, 'Task': Task, 'Goal': Goal}

if __name__ == '__main__':
    app.run(debug=True)
