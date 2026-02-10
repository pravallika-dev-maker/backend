from sqlalchemy import create_engine, text
import sys

# DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"
# Use Pooler URL for better remote connection
DATABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def check():
    print(f"Connecting to: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
        with engine.connect() as conn:
            print("Successfully connected!")
            
            tables = ["projects", "stages", "stage_history", "resources", "authorized_users"]
            
            for table in tables:
                print(f"\nChecking table: {table}")
                try:
                    # Check columns
                    res = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}'"))
                    cols = res.fetchall()
                    if not cols:
                        print("  Table not found or no columns!")
                        continue
                    
                    for col in cols:
                        print(f"  - {col[0]} ({col[1]})")
                    
                    # Check row count
                    res = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = res.scalar()
                    print(f"  TOTAL ROWS: {count}")
                    
                    if count > 0:
                        print("  SAMPLE DATA (Last 1):")
                        res = conn.execute(text(f"SELECT * FROM {table} LIMIT 1"))
                        print(f"    {res.fetchone()}")
                        
                except Exception as table_e:
                    print(f"  Error checking table {table}: {table_e}")
                    
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check()
