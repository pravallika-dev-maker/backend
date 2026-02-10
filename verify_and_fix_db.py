import psycopg2
import sys

# The ORIGINAL connection string that worked
ORIGINAL_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def verify_and_fix():
    print(f"Connecting to: {ORIGINAL_URL}")
    try:
        conn = psycopg2.connect(ORIGINAL_URL, connect_timeout=10)
        cur = conn.cursor()
        print("✅ Connected!")

        # 1. Check if parent_record_id exists
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='projects' AND column_name='parent_record_id'")
        if not cur.fetchone():
            print("Adding missing column 'parent_record_id'...")
            cur.execute("ALTER TABLE projects ADD COLUMN parent_record_id TEXT")
            conn.commit()
            print("✅ Column added.")
        else:
            print("✅ Column 'parent_record_id' already exists.")

        # 2. Check stages
        cur.execute("SELECT COUNT(*) FROM stages")
        print(f"✅ Stages count: {cur.fetchone()[0]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_and_fix()
