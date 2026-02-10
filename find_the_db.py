import sqlite3
import os

def check_db(path):
    print(f"\nChecking: {path}")
    if not os.path.exists(path):
        print("Does not exist")
        return
    print(f"Size: {os.path.getsize(path)} bytes")
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in c.fetchall() if t[0] != 'sqlite_sequence']
        print(f"Tables: {tables}")
        for t in tables:
            c.execute(f"SELECT COUNT(*) FROM {t}")
            print(f"  {t}: {c.fetchone()[0]} rows")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

check_db("sql_app.db")
check_db(os.path.join("backend", "sql_app.db"))
