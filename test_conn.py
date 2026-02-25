from sqlalchemy import create_engine, text
DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
try:
    with engine.connect() as conn:
        print("Connected!")
        res = conn.execute(text("SELECT current_database()"))
        print(f"DB: {res.scalar()}")
except Exception as e:
    print(f"Error: {e}")
