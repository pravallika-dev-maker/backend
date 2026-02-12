"""
Migration script to add missing columns to Supabase PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

print(f"Connecting to database...")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("\n=== Checking and updating 'users' table ===")
        
        # Check and add access_level column
        try:
            result = conn.execute(text("SELECT access_level FROM users LIMIT 1"))
            print("✓ Column 'access_level' already exists in users table")
        except Exception:
            print("Adding 'access_level' column to users table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN access_level VARCHAR DEFAULT 'READ'"))
            conn.commit()
            print("✓ Column 'access_level' added successfully")
        
        # Check and add can_add_users column
        try:
            result = conn.execute(text("SELECT can_add_users FROM users LIMIT 1"))
            print("✓ Column 'can_add_users' already exists in users table")
        except Exception:
            print("Adding 'can_add_users' column to users table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN can_add_users BOOLEAN DEFAULT FALSE"))
            conn.commit()
            print("✓ Column 'can_add_users' added successfully")
        
        print("\n=== Checking and updating 'resources' table ===")
        
        # Check and add email column
        try:
            result = conn.execute(text("SELECT email FROM resources LIMIT 1"))
            print("✓ Column 'email' already exists in resources table")
        except Exception:
            print("Adding 'email' column to resources table...")
            conn.execute(text("ALTER TABLE resources ADD COLUMN email VARCHAR"))
            conn.commit()
            print("✓ Column 'email' added successfully")
        
        # Check and add access_level column
        try:
            result = conn.execute(text("SELECT access_level FROM resources LIMIT 1"))
            print("✓ Column 'access_level' already exists in resources table")
        except Exception:
            print("Adding 'access_level' column to resources table...")
            conn.execute(text("ALTER TABLE resources ADD COLUMN access_level VARCHAR DEFAULT 'READ'"))
            conn.commit()
            print("✓ Column 'access_level' added successfully")
        
        print("\n=== Verifying schema ===")
        
        # Verify users table
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """))
        print("\nUsers table columns:")
        for row in result:
            print(f"  - {row[0]}: {row[1]} (default: {row[2]})")
        
        # Verify resources table
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'resources' 
            ORDER BY ordinal_position
        """))
        print("\nResources table columns:")
        for row in result:
            print(f"  - {row[0]}: {row[1]} (default: {row[2]})")
        
        print("\n✅ Database migration completed successfully!")
        
except Exception as e:
    print(f"\n❌ Error during migration: {e}")
    import traceback
    traceback.print_exc()
