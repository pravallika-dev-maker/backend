import sqlite3
import requests
import os
import sys

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_log.txt")

def log(msg):
    print(msg)
    with open(log_file, "a") as f:
        f.write(msg + "\n")

def manual_sync():
    if os.path.exists(log_file): os.remove(log_file)
    log("Starting manual sync...")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "sql_app.db")
    BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

    log(f"Target DB: {DB_PATH}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
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

        log("Fetching Projects from Sheet...")
        p_resp = requests.get(f"{BASE_SHEET_URL}/Projects_Deals")
        log(f"Projects Status: {p_resp.status_code}")
        p_data = p_resp.json()
        
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

        log(f"Inserted {len(p_data)} projects")

        log("Fetching Stages...")
        s_data = requests.get(f"{BASE_SHEET_URL}/Stage_Master").json()
        for s in s_data:
            cursor.execute("INSERT INTO stages (stage_name, stage_order) VALUES (?, ?)", 
                           (s.get('stage_name'), int(s.get('stage_order', 99))))
        log(f"Inserted {len(s_data)} stages")

        conn.commit()
        conn.close()
        log("Sync COMPLETE!")
    except Exception as e:
        log(f"ERROR: {e}")

if __name__ == "__main__":
    manual_sync()
