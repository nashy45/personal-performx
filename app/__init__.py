"""Flask application factory"""
import os
import logging
import sqlite3
from flask import Flask
from flask_login import LoginManager
from app.models import db, User
from config import config_dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _run_migrations(app):
    """Apply any missing columns that db.create_all() won't add to existing tables."""
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    # Robustly extract the file path from sqlite:/// or sqlite:////
    if not uri.startswith('sqlite:///'):
        return  # not SQLite – skip
    db_path = uri[len('sqlite:///'):]
    # On Windows the URI is sqlite:///C:\... so stripping 3 slashes gives C:\...
    # On Unix the URI is sqlite:////abs/path so stripping 3 slashes gives /abs/path
    # Both cases are handled correctly above.

    migrations = [
        ("goal", "completed", "BOOLEAN NOT NULL DEFAULT 0"),
        ("task", "priority",  "VARCHAR(10) DEFAULT 'Medium'"),
    ]
    try:
        conn = sqlite3.connect(db_path)
        cur  = conn.cursor()
        for table, column, col_def in migrations:
            cur.execute(f"PRAGMA table_info({table})")
            existing = [row[1] for row in cur.fetchall()]
            if column not in existing:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
                logger.info(f"Migration: added column '{column}' to table '{table}'")
        conn.commit()
        conn.close()
    except Exception as exc:
        logger.warning(f"Migration warning: {exc}")

def create_app(config_name='development'):
    """Application factory function"""
    
    # Get config
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    config = config_dict.get(config_name, config_dict['development'])
    
    # Create Flask app (use instance folder for configs and database)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)
    
    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception as exc:
        logger.warning(f"Could not create instance folder: {exc}")
    
    # Load configuration object
    app.config.from_object(config)
    
    # use absolute path for sqlite to avoid relative path issues
    # when the config defines a sqlite URI, convert to absolute based on instance path
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if uri.startswith('sqlite:///'):
        db_path = os.path.join(app.instance_path, 'database.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    # Initialize Database
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page"
    login_manager.login_message_category = "info"
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import auth_bp, tasks_bp, goals_bp, dashboard_bp, profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    
    # Create tables - explicitly import all models first so create_all sees them
    with app.app_context():
        from app.models.user import User
        from app.models.task import Task
        from app.models.goal import Goal
        db.create_all()
        _run_migrations(app)
        logger.info("✅ Database tables created successfully!")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {error}")
        return {"error": "Internal server error"}, 500
    
    return app
