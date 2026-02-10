from sqlalchemy import create_engine, text

# Supabase URL - using Pooler for reliability
DATABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def seed_essential_data():
    print("Connecting to Supabase...")
    try:
        engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
        with engine.connect() as conn:
            # 1. Ensure tables exist (run migrations manually just in case)
            print("Ensuring columns exist...")
            conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS parent_record_id VARCHAR"))
            conn.execute(text("ALTER TABLE stage_history ADD COLUMN IF NOT EXISTS stage_status VARCHAR"))
            conn.commit()

            # 2. Check stages
            res = conn.execute(text("SELECT COUNT(*) FROM stages"))
            count = res.scalar()
            
            if count == 0:
                print("Stages table is empty. Seeding default stages...")
                stages = [
                    ('Idea / Opportunity', 1),
                    ('Proposal / Quote', 2),
                    ('Negotiation', 3),
                    ('Under Execution', 4),
                    ('Completed', 5),
                    ('Closed', 6)
                ]
                for name, order in stages:
                    conn.execute(text("INSERT INTO stages (stage_name, stage_order) VALUES (:name, :order)"), {"name": name, "order": order})
                conn.commit()
                print(f"✅ Seeded {len(stages)} stages.")
            else:
                print(f"Stages already present ({count} rows).")

            # 3. Check if current projects have valid record IDs
            print("Verifying projects...")
            res = conn.execute(text("SELECT record_id, client_name FROM projects"))
            for row in res:
                print(f"  Existing Project: {row[0]} - {row[1]}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    seed_essential_data()
