import os
from sqlalchemy import create_engine, text

# Database URL from database.py
DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def migrate():
    print("Connecting to Supabase PostgreSQL...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("Checking for 'stage_status' column in 'stage_history'...")
        
        # Check if column exists
        query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='stage_history' AND column_name='stage_status';
        """)
        result = conn.execute(query).fetchone()
        
        if not result:
            print("Adding 'stage_status' column...")
            conn.execute(text("ALTER TABLE stage_history ADD COLUMN stage_status VARCHAR;"))
            conn.commit()
            print("Migration successful.")
        else:
            print("'stage_status' column already exists.")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"Error: {e}")
