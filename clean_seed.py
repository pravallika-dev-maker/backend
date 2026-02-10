import sqlite3
import os

db_path = 'sql_app.db'

def seed():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop and recreate tables to ensure clean state
    cursor.execute('DROP TABLE IF EXISTS projects')
    cursor.execute('DROP TABLE IF EXISTS stages')
    cursor.execute('DROP TABLE IF EXISTS users')
    
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

    cursor.execute('''
    CREATE TABLE stages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_name TEXT,
        stage_order INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        hashed_password TEXT
    )
    ''')

    # Insert mock data
    projects = [
        ('REC101', 'Acme Corp', 'Project', 500000.0, 'John Doe', 'Proposal', 'Negotiation', '2026-03-01', 'Active', 'Strategic Planning', '2026-01-15'),
        ('REC102', 'Global Tech', 'Project', 1200000.0, 'Jane Smith', 'Execution', 'Closing', '2026-04-15', 'Active', 'On Track', '2025-12-01'),
        ('REC103', 'Nexus Inc', 'Project', 300000.0, 'Bob Lee', 'Lead', 'Contacted', '2026-05-01', 'Active', 'Initial Outreach', '2026-02-01'),
    ]
    
    for p in projects:
        cursor.execute('''
        INSERT INTO projects (record_id, client_name, deal_type, deal_value, project_owner_name, current_stage_name, next_stage_name, next_stage_expected_date, deal_status, execution_status, project_started_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', p)

    stages = [
        ('Lead', 1),
        ('Contacted', 2),
        ('Proposal', 3),
        ('Negotiation', 4),
        ('Closing', 5),
        ('Execution', 6)
    ]
    
    for s in stages:
        cursor.execute('INSERT INTO stages (stage_name, stage_order) VALUES (?, ?)', s)
        
    # Seed Admin User
    cursor.execute('INSERT INTO users (full_name, email, hashed_password) VALUES (?, ?, ?)', 
                   ('Admin User', 'admin@example.com', 'password123'))
            
    conn.commit()
    conn.close()
    print("Clean SQLite seed completed.")

if __name__ == "__main__":
    seed()
