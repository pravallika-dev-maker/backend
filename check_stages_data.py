from sqlalchemy import create_engine, text

# Using the hardcoded URL from database.py for consistency
DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def check_stages():
    print(f"Connecting to Supabase to check stages...")
    try:
        engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, stage_name, stage_order FROM stages ORDER BY stage_order"))
            rows = result.fetchall()
            print(f"\nFOUND {len(rows)} STAGES:")
            for row in rows:
                print(f"  ID: {row[0]} | Name: '{row[1]}' | Order: {row[2]}")
            
            if not rows:
                print("\n⚠️ WARNING: The stages table is EMPTY! This will cause project creation to fail.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_stages()
