import psycopg2
import os

# Supabase connection string
# Using the same one from migrate_to_supabase.py for consistency if needed, 
# but better to use the environment variable if available.
SUPABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")

def setup_finance_tables():
    print("Connecting to Supabase...")
    try:
        conn = psycopg2.connect(SUPABASE_URL)
        cur = conn.cursor()
        print("Connected!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # 1. Create project_financials if not exists
    print("Creating project_financials table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_financials (
            id SERIAL PRIMARY KEY,
            project_id TEXT,
            project_category TEXT,
            monthly_billing_amount NUMERIC,
            billing_owner TEXT,
            billing_start_date TEXT,
            billing_end_date TEXT
        );
    """)

    # 2. Create cost_items if not exists
    print("Creating cost_items table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cost_items (
            id SERIAL PRIMARY KEY,
            cost_name TEXT,
            cost_category TEXT,
            monthly_amount NUMERIC,
            owner_name TEXT,
            start_date TEXT,
            end_date TEXT
        );
    """)

    # 3. Create funds table
    print("Creating funds table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS funds (
            id SERIAL PRIMARY KEY,
            investor_name TEXT,
            funding_amount NUMERIC,
            funding_date TEXT,
            funding_type TEXT,
            responsible_owner TEXT,
            notes TEXT
        );
    """)

    # 4. Insert dummy data for funds if empty
    cur.execute("SELECT COUNT(*) FROM funds")
    if cur.fetchone()[0] == 0:
        print("Seeding dummy data for funds...")
        funds_data = [
            ('Falcon VC', 5000000, '2026-02-12', 'Seed', 'Vijay', 'Initial seed round for expansion'),
            ('Internal', 1000000, '2026-03-05', 'Internal', 'Vijay', 'Internal bridge funding'),
            ('Angel Investor (S. Kumar)', 2500000, '2026-04-20', 'Angel', 'Vijay', 'Pre-series A focus'),
        ]
        for f in funds_data:
            cur.execute("""
                INSERT INTO funds (investor_name, funding_amount, funding_date, funding_type, responsible_owner, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, f)

    # 5. Insert some dummy data for cost_items if empty (to satisfy "Fixed Costs" requirement)
    cur.execute("SELECT COUNT(*) FROM cost_items")
    if cur.fetchone()[0] == 0:
        print("Seeding dummy data for cost_items...")
        costs_data = [
            ('Office Rent - Bangalore', 'Rent', 150000, 'Vijay', '2026-01-01', '2026-12-31'),
            ('Core Team Salaries', 'Salary', 1200000, 'Kiran', '2026-01-01', '2026-12-31'),
            ('AWS Infrastructure', 'Server', 45000, 'Prashant', '2026-01-01', '2026-12-31'),
            ('SaaS Tools (Slack/Zoom)', 'Tools', 15000, 'Kiran', '2026-01-01', '2026-12-31'),
        ]
        for c in costs_data:
            cur.execute("""
                INSERT INTO cost_items (cost_name, cost_category, monthly_amount, owner_name, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, c)

    conn.commit()
    cur.close()
    conn.close()
    print("Finance tables setup and seeding completed!")

if __name__ == "__main__":
    setup_finance_tables()
