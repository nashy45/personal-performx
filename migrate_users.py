"""
Database Migration Script - Export users from old app to new app
"""
import sqlite3
import os
from pathlib import Path
from werkzeug.security import generate_password_hash

def export_users_from_old_db():
    """Try to export users from old database format"""
    
    # Try different possible locations for old database
    possible_locations = [
        Path(__file__).parent / "database.db",
        Path(__file__).parent / "app.db",
        Path(__file__).parent / "performx.db",
    ]
    
    old_db_path = None
    for path in possible_locations:
        if path.exists():
            old_db_path = path
            break
    
    if not old_db_path:
        print("❌ Could not find old database file")
        print(f"   Checked: {[str(p) for p in possible_locations]}")
        return None
    
    print(f"✅ Found old database at: {old_db_path}")
    
    try:
        conn = sqlite3.connect(old_db_path)
        cursor = conn.cursor()
        
        # Try to get users from old database
        cursor.execute("SELECT id, full_name, email, password FROM user")
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            print("❌ No users found in old database")
            return None
        
        print(f"✅ Found {len(users)} users:")
        for user_id, full_name, email, password_hash in users:
            print(f"   - {email} ({full_name})")
        
        return users
    
    except Exception as e:
        print(f"❌ Error reading old database: {e}")
        return None

def import_users_to_new_db(users):
    """Import users to new database"""
    from app import create_app
    from app.models import db, User
    
    app = create_app('development')
    
    with app.app_context():
        imported = 0
        skipped = 0
        
        for user_id, full_name, email, password_hash in users:
            # Check if user already exists
            existing = User.query.filter_by(email=email).first()
            if existing:
                print(f"⚠️  Skipped {email} (already exists)")
                skipped += 1
                continue
            
            # Create new user with old password hash
            try:
                new_user = User(
                    full_name=full_name,
                    email=email,
                    password=password_hash  # Keep original hash
                )
                db.session.add(new_user)
                db.session.commit()
                print(f"✅ Imported: {email}")
                imported += 1
            except Exception as e:
                db.session.rollback()
                print(f"❌ Failed to import {email}: {e}")
        
        print(f"\n📊 Summary: {imported} imported, {skipped} skipped")
        return imported > 0

def main():
    print("=" * 60)
    print("Database Migration Tool")
    print("=" * 60)
    
    # Try to export from old database
    users = export_users_from_old_db()
    
    if not users:
        print("\n" + "=" * 60)
        print("BACKUP NOT FOUND")
        print("=" * 60)
        print("\nSince we can't find your old database, you have options:")
        print("\n1. RECREATE USERS MANUALLY")
        print("   - Use the /register page to create accounts")
        print("   - Use the same email/password as before")
        print("\n2. RESTORE FROM BACKUP")
        print("   - If you have the old database.db file,")
        print("   - Copy it to: instance/database.db")
        print("   - Then restart the app")
        print("\n3. EXPORT DATA FROM OLD APP")
        print("   - Keep the old app.py running on different port")
        print("   - Export users manually")
        
        user_choice = input("\nWhich option? (1/2/3): ").strip()
        
        if user_choice == "1":
            print("\n📝 To recreate users:")
            print("   1. Start the app: python run.py")
            print("   2. Go to: http://localhost:5000/register")
            print("   3. Create accounts with same credentials as before")
        elif user_choice == "2":
            print("\n💾 To restore from backup:")
            print("   Copy your old database.db to:")
            print("   c:\\Users\\fombu\\OneDrive\\Desktop\\performx\\instance\\database.db")
        elif user_choice == "3":
            print("\n🔄 To use old app:")
            print("   1. Use old app.py temporarily")
            print("   2. Export user data (email/password pairs)")
            print("   3. Re-import to new app")
        return False
    
    # Found users, offer to import
    print("\n" + "=" * 60)
    response = input(f"\nImport these {len(users)} users to new database? (yes/no): ").strip().lower()
    
    if response == 'yes':
        if import_users_to_new_db(users):
            print("\n✅ Users imported successfully!")
            print("   You can now log in with your old credentials.")
        else:
            print("\n❌ Import failed")
        return True
    else:
        print("Cancelled.")
        return False

if __name__ == '__main__':
    main()
