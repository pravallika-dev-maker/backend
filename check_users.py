from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def check_users():
    print(f"Connecting to: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
        with engine.connect() as conn:
            print("Successfully connected!")
            
            # Check users table
            res = conn.execute(text("SELECT email, full_name, can_add_users FROM users"))
            rows = res.fetchall()
            print(f"\nTOTAL USERS: {len(rows)}")
            for row in rows:
                print(f"  - {row[0]} | {row[1]} | CEO: {row[2]}")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_users()
