from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("--- Funds Table Structure ---")
    res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'funds'"))
    for row in res:
        print(f"Column: {row[0]}, Type: {row[1]}")
    
    print("\n--- Funds Data Snapshot ---")
    res = conn.execute(text("SELECT * FROM funds LIMIT 5"))
    cols = res.keys()
    print(cols)
    for row in res:
        print(row)

    print("\n--- Costs Total Calculation ---")
    res = conn.execute(text("SELECT SUM(monthly_amount) FROM costs"))
    total_costs = res.scalar()
    print(f"Total Monthly Amount for Costs: {total_costs}")
