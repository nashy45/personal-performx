"""
Setup database schema and recreate users
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash
from pathlib import Path

def setup_database():
    """Create database schema"""
    db_path = Path('instance/database.db')
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create user table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS [user] (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name VARCHAR(150) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(200) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create goal table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(150) NOT NULL,
                description TEXT,
                target_date DATETIME,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES [user] (id)
            )
        ''')
        
        # Create task table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(150) NOT NULL,
                description TEXT,
                due_date DATETIME,
                priority VARCHAR(10) DEFAULT 'Medium',
                completed BOOLEAN DEFAULT 0,
                user_id INTEGER NOT NULL,
                goal_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES [user] (id),
                FOREIGN KEY (goal_id) REFERENCES goal (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database schema created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        return False

def add_user():
    """Interactively add users"""
    db_path = Path('instance/database.db')
    
    if not db_path.exists():
        print("❌ Database not found. Run setup first.")
        return
    
    print("\n" + "=" * 60)
    print("Add Users to Database")
    print("=" * 60)
    print("Leave email blank when done.\n")
    
    users_added = 0
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        while True:
            email = input("Email (or press Enter to finish): ").strip().lower()
            
            if not email:
                break
            
            if '@' not in email:
                print("❌ Invalid email format\n")
                continue
            
            # Check if exists
            cursor.execute("SELECT id FROM [user] WHERE email = ?", (email,))
            if cursor.fetchone():
                print(f"⚠️  {email} already exists\n")
                continue
            
            full_name = input("Full Name: ").strip()
            if not full_name:
                print("❌ Full name required\n")
                continue
            
            password = input("Password: ").strip()
            if len(password) < 6:
                print("❌ Password must be at least 6 characters\n")
                continue
            
            hashed = generate_password_hash(password)
            
            try:
                cursor.execute(
                    "INSERT INTO [user] (full_name, email, password) VALUES (?, ?, ?)",
                    (full_name, email, hashed)
                )
                conn.commit()
                print(f"✅ Created: {email}\n")
                users_added += 1
            except Exception as e:
                print(f"❌ Error: {e}\n")
        
        conn.close()
        print("=" * 60)
        print(f"✅ Added {users_added} user(s)")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    setup_database()
    add_user()
