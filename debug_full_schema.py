from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def check_all_schema():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Checking all tables in public schema...")
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row[0] for row in result]
        
        for table in tables:
            print(f"\nTABLE: {table}")
            result = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}'"))
            cols = [(row[0], row[1]) for row in result]
            for name, dtype in cols:
                print(f"  {name}: {dtype}")

if __name__ == "__main__":
    check_all_schema()
