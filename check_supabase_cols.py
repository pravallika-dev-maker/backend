from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

def check():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='stage_history'"))
        cols = [row[0] for row in result]
        print(f"COLUMNS: {cols}")

if __name__ == "__main__":
    check()
