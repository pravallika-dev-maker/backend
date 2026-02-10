import requests
import psycopg2
from psycopg2.extras import execute_values
import os

# NOTE: Replace with your actual Supabase connection string
# It usually looks like: postgresql://postgres.xxxx:password@aws-0-region.pooler.supabase.com:6543/postgres
SUPABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

# Google Sheet URLs
BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

def sync_to_supabase(connection_string):
    print("Connecting to Supabase...")
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        print("Connected!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # 1. Create Tables
    print("Creating tables if not exist...")
    
    # Users Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name TEXT,
            email TEXT UNIQUE,
            hashed_password TEXT
        );
    """)

    # Stages Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stages (
            id SERIAL PRIMARY KEY,
            stage_name TEXT,
            stage_order INTEGER
        );
    """)

    # Projects Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            record_id TEXT UNIQUE,
            client_name TEXT,
            deal_type TEXT,
            deal_value FLOAT,
            project_owner_name TEXT,
            current_stage_name TEXT,
            next_stage_name TEXT,
            next_stage_expected_date TEXT,
            deal_status TEXT,
            execution_status TEXT,
            project_started_date TEXT
        );
    """)
    
    # Resources Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id SERIAL PRIMARY KEY,
            resource_name TEXT,
            role TEXT,
            assigned_record_id TEXT
        );
    """)

    # History Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stage_history (
            id SERIAL PRIMARY KEY,
            record_id TEXT,
            stage_name TEXT,
            stage_start_date TEXT,
            stage_end_date TEXT
        );
    """)
    
    conn.commit()

    # 2. Fetch Data from Google Sheets
    print("Fetching data from Google Sheets...")
    
    projects_data = requests.get(f"{BASE_SHEET_URL}/Projects_Deals").json()
    stages_data = requests.get(f"{BASE_SHEET_URL}/Stage_Master").json()
    resources_data = requests.get(f"{BASE_SHEET_URL}/Resources").json()
    history_data = requests.get(f"{BASE_SHEET_URL}/Stage_History").json()

    # 3. Insert Data
    print("Inserting data into Supabase...")

    # Clear existing data first (optional, safer for re-running)
    cur.execute("TRUNCATE TABLE projects, stages, resources, stage_history RESTART IDENTITY;")
    
    # Insert Projects
    project_tuples = []
    for p in projects_data:
        val = p.get('deal_value', 0)
        if isinstance(val, str):
            val = float(val.replace(',', '') or 0)
            
        project_tuples.append((
            p.get('record_id'),
            p.get('client_name'),
            p.get('deal_type'),
            val,
            p.get('project_owner_name'),
            p.get('current_stage_name'),
            p.get('next_stage_name'),
            p.get('next_stage_expected_date'),
            p.get('deal_status', 'Active'),
            p.get('execution_status', 'In Progress'),
            p.get('project_started_date', '2026-01-01')
        ))
    
    execute_values(cur, """
        INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, 
        current_stage_name, next_stage_name, next_stage_expected_date, deal_status, 
        execution_status, project_started_date) VALUES %s
    """, project_tuples)

    # Insert Stages
    stage_tuples = [(s.get('Idea / Opportunity'), int(s.get('stage_order', 99))) for s in stages_data if s.get('Idea / Opportunity')]
    execute_values(cur, "INSERT INTO stages (stage_name, stage_order) VALUES %s", stage_tuples)

    # Insert Resources
    resource_tuples = [(
        r.get('resource_name') or r.get('name'), 
        r.get('role'), 
        r.get('assigned_record_id')
    ) for r in resources_data]
    execute_values(cur, "INSERT INTO resources (resource_name, role, assigned_record_id) VALUES %s", resource_tuples)

    # Insert History
    history_tuples = [(
        h.get('record_id'),
        h.get('stage_name'),
        h.get('stage_start_date') or h.get('transition_date'),
        h.get('stage_end_date') or h.get('transition_date')
    ) for h in history_data]
    execute_values(cur, "INSERT INTO stage_history (record_id, stage_name, stage_start_date, stage_end_date) VALUES %s", history_tuples)

    # Insert default admin user
    try:
        cur.execute("""
            INSERT INTO users (full_name, email, hashed_password) 
            VALUES ('Admin User', 'admin@example.com', 'password123')
            ON CONFLICT (email) DO NOTHING;
        """)
    except Exception:
        pass # User might already exist

    conn.commit()
    cur.close()
    conn.close()
    print("Supabase migration completed successfully!")

if __name__ == "__main__":
    # Ask user for connection string if not hardcoded
    import sys
    if len(sys.argv) > 1:
        conn_str = sys.argv[1]
    else:
        conn_str = input("Enter your Supabase Connection String: ")
    
    sync_to_supabase(conn_str)
