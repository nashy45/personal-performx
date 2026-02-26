"""User service for user-related operations"""
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app.utils.validators import validate_email, validate_password

class UserService:
    """Service class for user operations"""

    @staticmethod
    def register_user(full_name, email, password, confirm_password):
        if not full_name or not email or not password:
            return False, "All fields are required"
        if not validate_email(email):
            return False, "Invalid email format"
        if password != confirm_password:
            return False, "Passwords do not match"
        is_valid, msg = validate_password(password)
        if not is_valid:
            return False, msg
        if User.query.filter_by(email=email).first():
            return False, "Email already registered"
        try:
            new_user = User(full_name=full_name, email=email,
                            password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return True, "Registration successful"
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}"

    @staticmethod
    def login_user(email, password):
        if not email or not password:
            return None, "Email and password are required"
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user, "Login successful"
        return None, "Invalid email or password"

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_profile(user_id, full_name):
        """Update user's display name"""
        if not full_name or not full_name.strip():
            return False, "Name cannot be empty"
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        try:
            user.full_name = full_name.strip()
            db.session.commit()
            return True, "Profile updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Error updating profile: {str(e)}"

    @staticmethod
    def change_password(user_id, current_password, new_password, confirm_password):
        """Change user's password"""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        if not check_password_hash(user.password, current_password):
            return False, "Current password is incorrect"
        if new_password != confirm_password:
            return False, "New passwords do not match"
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return False, msg
        try:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return True, "Password changed successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Error changing password: {str(e)}"
