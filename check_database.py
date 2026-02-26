"""
Quick database diagnostic and fix script
"""
import os
import shutil
from pathlib import Path

project_root = Path(__file__).parent

# Check where databases exist
root_db = project_root / "database.db"
instance_db = project_root / "instance" / "database.db"

print("Database Location Check:")
print(f"Root database exists: {root_db.exists()}")
print(f"Instance database exists: {instance_db.exists()}")

if root_db.exists():
    print(f"\n✅ Found old database at: {root_db}")
    print(f"Size: {root_db.stat().st_size} bytes")
    
    # Offer to move it
    response = input("\nWould you like to move this to the new location? (yes/no): ").strip().lower()
    if response == 'yes':
        # Backup the instance database first
        if instance_db.exists():
            backup = project_root / "instance" / "database.db.backup"
            shutil.copy2(instance_db, backup)
            print(f"✅ Backed up new database to: {backup}")
        
        # Move old database
        shutil.move(str(root_db), str(instance_db))
        print(f"✅ Moved database to: {instance_db}")
        print("\nYour old user data is now available in the new app!")
        print("Try logging in again.")
else:
    print(f"\n❌ No old database found at: {root_db}")
    print("\nYou can either:")
    print("1. Register a new account")
    print("2. Restore from backup if you have one")

# Show current database info
if instance_db.exists():
    print(f"\n📊 Current database at: {instance_db}")
    print(f"Size: {instance_db.stat().st_size} bytes")
