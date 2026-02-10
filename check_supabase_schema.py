from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def check_table(table_name):
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print(f"\nTABLE: {table_name}")
        result = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table_name}'"))
        cols = [(row[0], row[1]) for row in result]
        for name, dtype in cols:
            print(f"  {name}: {dtype}")
        
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        print(f"  Total ROWS: {result.fetchone()[0]}")

if __name__ == "__main__":
    check_table("projects")
    check_table("stages")
    check_table("stage_history")
    check_table("resources")
