import sqlite3
import os
import time

# Robust path finding
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sql_app.db")
print(f"Target DB: {DB_PATH}")

def run():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects';")
    if not cursor.fetchone():
        print("Creating table projects...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT UNIQUE,
            client_name TEXT,
            deal_type TEXT,
            deal_value REAL,
            project_owner_name TEXT,
            current_stage_name TEXT,
            next_stage_name TEXT,
            next_stage_expected_date TEXT,
            deal_status TEXT,
            execution_status TEXT,
            project_started_date TEXT
        )
        ''')
    
    # Check count
    cursor.execute("SELECT COUNT(*) FROM projects")
    count = cursor.fetchone()[0]
    print(f"Current project count: {count}")
    
    if count == 0:
        print("Seeding mock data...")
        projects = [
            ('REC101', 'Acme Corp', 'Project', 500000.0, 'John Doe', 'Proposal', 'Negotiation', '2026-03-01', 'Active', 'Strategic Planning', '2026-01-15'),
            ('REC102', 'Global Tech', 'Project', 1200000.0, 'Jane Smith', 'Execution', 'Closing', '2026-04-15', 'Active', 'On Track', '2025-12-01'),
            ('REC103', 'Nexus Inc', 'Project', 300000.0, 'Bob Lee', 'Lead', 'Contacted', '2026-05-01', 'Active', 'Initial Outreach', '2026-02-01'),
        ]
        try:
            for p in projects:
                cursor.execute('''
                INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, current_stage_name, next_stage_name, next_stage_expected_date, deal_status, execution_status, project_started_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', p)
            conn.commit()
            print("Seeded 3 projects.")
        except Exception as e:
            print(f"Error seeding: {e}")
            
    conn.close()

if __name__ == "__main__":
    run()
