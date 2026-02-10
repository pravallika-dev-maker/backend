import sqlite3
import requests
import os

# Robust absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sql_app.db")
BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

def manual_sync():
    print(f"Syncing data to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure tables exist (minimal schema based on models)
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute('''
    CREATE TABLE projects (
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
    
    cursor.execute("DROP TABLE IF EXISTS stages")
    cursor.execute("CREATE TABLE stages (id INTEGER PRIMARY KEY AUTOINCREMENT, stage_name TEXT, stage_order INTEGER)")

    # Fetch and Insert
    print("Fetching Projects...")
    p_data = requests.get(f"{BASE_SHEET_URL}/Projects_Deals").json()
    for p in p_data:
        cursor.execute('''
        INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, 
                             current_stage_name, next_stage_name, next_stage_expected_date, 
                             deal_status, execution_status, project_started_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p.get('record_id'), p.get('client_name'), p.get('deal_type'),
            float(str(p.get('deal_value', 0)).replace(',', '') or 0),
            p.get('project_owner_name'), p.get('current_stage_name'), 
            p.get('next_stage_name'), p.get('next_stage_expected_date'),
            p.get('deal_status'), p.get('execution_status'), p.get('project_started_date')
        ))

    print("Fetching Stages...")
    s_data = requests.get(f"{BASE_SHEET_URL}/Stage_Master").json()
    for s in s_data:
        cursor.execute("INSERT INTO stages (stage_name, stage_order) VALUES (?, ?)", 
                       (s.get('stage_name'), int(s.get('stage_order', 99))))

    conn.commit()
    conn.close()
    print("Sync complete!")

if __name__ == "__main__":
    manual_sync()
