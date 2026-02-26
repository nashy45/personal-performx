"""
Manual User Recreation Tool
Run this to recreate your users in the new database
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

def recreate_users():
    """Interactively recreate users"""
    try:
        app = create_app('development')
    except Exception as e:
        print(f"❌ Error initializing app: {e}")
        return
    
    with app.app_context():
        users_created = 0
        
        print("=" * 60)
        print("Manual User Recreation Tool")
        print("=" * 60)
        print("\nEnter your users' credentials below.")
        print("Leave email blank when done.\n")
        
        while True:
            email = input("Email (or press Enter to finish): ").strip().lower()
            
            if not email:
                break
            
            # Check if user already exists
            try:
                existing = User.query.filter_by(email=email).first()
                if existing:
                    print(f"⚠️  {email} already exists, skipping\n")
                    continue
            except Exception as e:
                print(f"❌ Database error: {e}\n")
                continue
            
            full_name = input("Full Name: ").strip()
            if not full_name:
                print("❌ Full name required, skipping\n")
                continue
            
            password = input("Password: ").strip()
            if not password:
                print("❌ Password required, skipping\n")
                continue
            
            if len(password) < 6:
                print("❌ Password must be at least 6 characters\n")
                continue
            
            try:
                hashed_password = generate_password_hash(password)
                new_user = User(
                    full_name=full_name,
                    email=email,
                    password=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()
                print(f"✅ Created user: {email}\n")
                users_created += 1
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating user: {e}\n")
        
        print("=" * 60)
        print(f"✅ Created {users_created} user(s) successfully!")
        print("=" * 60)
        print("\nYou can now log in with these credentials in the app.")

if __name__ == '__main__':
    recreate_users()
