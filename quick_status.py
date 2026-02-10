import psycopg2
import sys

# SUPABASE CONNECTION
DB_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def check():
    print(f"Checking Supabase table status...")
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=10)
        cur = conn.cursor()
        
        tables = ['projects', 'stages', 'stage_history', 'resources']
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"Table '{table}': {count} rows")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
