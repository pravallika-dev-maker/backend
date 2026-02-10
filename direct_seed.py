import sqlite3

def seed():
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    
    # Create projects table if not exists (though it should be there)
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

    # Insert mock data
    projects = [
        ('REC101', 'Test Client A', 'Project', 10000.0, 'Owner A', 'Lead', 'Contacted', '2026-03-01', 'Active', 'New', '2026-01-01'),
        ('REC102', 'Test Client B', 'project', 20000.0, 'Owner B', 'Proposal', 'Negotiation', '2026-03-15', 'Active', 'Pending', '2026-01-15'),
    ]
    
    for p in projects:
        try:
            cursor.execute('''
            INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, current_stage_name, next_stage_name, next_stage_expected_date, deal_status, execution_status, project_started_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', p)
        except Exception as e:
            print(f"Error inserting {p[0]}: {e}")
            
    conn.commit()
    conn.close()
    print("Direct SQLite seed info written.")

if __name__ == "__main__":
    seed()
