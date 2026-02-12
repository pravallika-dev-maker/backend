"""
Simple script to verify Supabase database schema
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

print("Connecting to Supabase database...")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("\n=== USERS TABLE SCHEMA ===")
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"  {row[0]}: {row[1]} (default: {row[2]})")
        
        print("\n=== RESOURCES TABLE SCHEMA ===")
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'resources' 
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"  {row[0]}: {row[1]} (default: {row[2]})")
        
        print("\n=== USERS DATA ===")
        result = conn.execute(text("SELECT full_name, email, access_level, can_add_users FROM users"))
        for row in result:
            print(f"  User: {row[0]}, Email: {row[1]}, Access: {row[2]}, CEO: {row[3]}")
        
        print("\n=== RESOURCES DATA ===")
        result = conn.execute(text("SELECT resource_name, email, role, access_level, assigned_record_id FROM resources"))
        for row in result:
            print(f"  Resource: {row[0]}, Email: {row[1]}, Role: {row[2]}, Access: {row[3]}, Project: {row[4]}")
        
        print("\nDatabase schema verification completed!")
        
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
