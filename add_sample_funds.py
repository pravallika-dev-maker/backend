from sqlalchemy import create_engine, text
from datetime import date

# Database URL from app/database.py
DATABASE_URL = "postgresql://postgres:QTFoSloCe0UxEomc@db.yibpjemrwzawgxdcnmsw.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

sample_funds = [
    {
        "investor_name": "Phoenix Ventures",
        "amount_raised": 15000000,
        "funding_date": "2024-01-15",
        "funding_type": "Equity",
        "owner_responsible": "Pravas",
        "notes": "Series A Funding Round"
    },
    {
        "investor_name": "Global Insight Partners",
        "amount_raised": 7500000,
        "funding_date": "2024-05-10",
        "funding_type": "Debt",
        "owner_responsible": "Pravas",
        "notes": "Convertible Note"
    },
    {
        "investor_name": "Angel Network Alpha",
        "amount_raised": 2500000,
        "funding_date": "2024-08-22",
        "funding_type": "Equity",
        "owner_responsible": "Pravas",
        "notes": "Seed Extension"
    }
]

def add_sample_data():
    with engine.connect() as conn:
        print("Cleaning old data...")
        conn.execute(text("DELETE FROM funds"))
        
        print("Inserting sample funds...")
        for fund in sample_funds:
            query = text("""
                INSERT INTO funds (investor_name, amount_raised, funding_date, funding_type, owner_responsible, notes)
                VALUES (:investor_name, :amount_raised, :funding_date, :funding_type, :owner_responsible, :notes)
            """)
            conn.execute(query, fund)
        
        conn.commit()
        print("Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data()
