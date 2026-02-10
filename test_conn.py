import psycopg2
import sys

# DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"
db_url = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

print(f"Connecting to {db_url}...")
try:
    conn = psycopg2.connect(db_url, connect_timeout=10)
    print("Connected!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print(f"Tables: {tables}")
    conn.close()
except Exception as e:
    print(f"Failed: {e}")
