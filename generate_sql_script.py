import requests
import json

BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

def generate_sql():
    print("Fetching data from Google Sheets...")
    projects = requests.get(f"{BASE_SHEET_URL}/Projects_Deals").json()
    stages = requests.get(f"{BASE_SHEET_URL}/Stage_Master").json()
    resources = requests.get(f"{BASE_SHEET_URL}/Resources").json()
    history = requests.get(f"{BASE_SHEET_URL}/Stage_History").json()

    sql_lines = []

    # --- 1. CLEANUP & SCHEMA ---
    sql_lines.append("-- 1. Cleanup existing tables (Optional, remove if you want to keep data)")
    sql_lines.append("DROP TABLE IF EXISTS stage_history;")
    sql_lines.append("DROP TABLE IF EXISTS resources;")
    sql_lines.append("DROP TABLE IF EXISTS projects;")
    sql_lines.append("DROP TABLE IF EXISTS stages;")
    sql_lines.append("DROP TABLE IF EXISTS users;")
    sql_lines.append("")

    sql_lines.append("-- 2. Create Users Table")
    sql_lines.append("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    email TEXT UNIQUE,
    hashed_password TEXT
);
""")

    sql_lines.append("-- 3. Create Stages Table")
    sql_lines.append("""
CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    stage_name TEXT,
    stage_order INTEGER
);
""")

    sql_lines.append("-- 4. Create Projects Table")
    sql_lines.append("""
CREATE TABLE projects (
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

    sql_lines.append("-- 5. Create Resources Table")
    sql_lines.append("""
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    resource_name TEXT,
    role TEXT,
    assigned_record_id TEXT
);
""")

    sql_lines.append("-- 6. Create Stage History Table")
    sql_lines.append("""
CREATE TABLE stage_history (
    id SERIAL PRIMARY KEY,
    record_id TEXT,
    stage_name TEXT,
    stage_start_date TEXT,
    stage_end_date TEXT
);
""")

    sql_lines.append("")
    sql_lines.append("-- 7. Insert Data")

    # --- USERS ---
    sql_lines.append("INSERT INTO users (full_name, email, hashed_password) VALUES ('Admin User', 'admin@example.com', 'password123') ON CONFLICT (email) DO NOTHING;")

    # --- STAGES ---
    if stages:
        values_list = []
        for s in stages:
            name = s.get('stage_name', '').replace("'", "''")
            order = int(s.get('stage_order', 99))
            values_list.append(f"('{name}', {order})")
        sql_lines.append(f"INSERT INTO stages (stage_name, stage_order) VALUES {', '.join(values_list)};")

    # --- PROJECTS ---
    if projects:
        # Batch insert for projects
        values_list = []
        for p in projects:
            val = p.get('deal_value', 0)
            if isinstance(val, str):
                val = val.replace(',', '') or 0
            
            # Helper to escape single quotes
            def esc(v): return str(v).replace("'", "''") if v else ''
            
            values_list.append(f"('{esc(p.get('record_id'))}', '{esc(p.get('client_name'))}', '{esc(p.get('deal_type'))}', {float(val)}, '{esc(p.get('project_owner_name'))}', '{esc(p.get('current_stage_name'))}', '{esc(p.get('next_stage_name'))}', '{esc(p.get('next_stage_expected_date'))}', '{esc(p.get('deal_status', 'Active'))}', '{esc(p.get('execution_status', 'In Progress'))}', '{esc(p.get('project_started_date', '2026-01-01'))}')")
        
        sql_lines.append(f"""
INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, current_stage_name, next_stage_name, next_stage_expected_date, deal_status, execution_status, project_started_date) 
VALUES 
{', '.join(values_list)};
""")

    # --- RESOURCES ---
    if resources:
        values_list = []
        for r in resources:
            def esc(v): return str(v).replace("'", "''") if v else ''
            name = esc(r.get('resource_name') or r.get('name'))
            role = esc(r.get('role'))
            rec_id = esc(r.get('assigned_record_id'))
            values_list.append(f"('{name}', '{role}', '{rec_id}')")
        sql_lines.append(f"INSERT INTO resources (resource_name, role, assigned_record_id) VALUES {', '.join(values_list)};")

    # --- HISTORY ---
    if history:
        values_list = []
        for h in history:
            def esc(v): return str(v).replace("'", "''") if v else ''
            rec_id = esc(h.get('record_id'))
            name = esc(h.get('stage_name'))
            start = esc(h.get('stage_start_date') or h.get('transition_date'))
            end = esc(h.get('stage_end_date') or h.get('transition_date'))
            values_list.append(f"('{rec_id}', '{name}', '{start}', '{end}')")
        sql_lines.append(f"INSERT INTO stage_history (record_id, stage_name, stage_start_date, stage_end_date) VALUES {', '.join(values_list)};")

    # Write to file
    with open("supabase_dump.sql", "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))
    
    print("SQL Dump generated: supabase_dump.sql")

if __name__ == "__main__":
    generate_sql()
