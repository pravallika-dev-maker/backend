import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'backend', 'sql_app.db')

def migrate():
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if stage_status column exists in stage_history
        cursor.execute("PRAGMA table_info(stage_history)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'stage_status' not in columns:
            print("Adding 'stage_status' column to 'stage_history' table...")
            cursor.execute("ALTER TABLE stage_history ADD COLUMN stage_status TEXT")
            conn.commit()
            print("Migration successful.")
        else:
            print("'stage_status' column already exists.")
            
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
