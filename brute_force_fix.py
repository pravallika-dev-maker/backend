import os
from sqlalchemy import create_engine, text

# Try potential Supabase hosts
HOSTS = [
    "aws-0-ap-south-1.pooler.supabase.com",
    "aws-1-ap-south-1.pooler.supabase.com",
    "db.yibpjemrwzawgxdcnmsw.supabase.co"
]
PASSWORD = "QTFoSloCe0UxEomc"
USER_ID = "postgres.yibpjemrwzawgxdcnmsw"
DB_NAME = "postgres"

def fix():
    for host in HOSTS:
        port = 6543 if "pooler" in host else 5432
        url = f"postgresql://{USER_ID}:{PASSWORD}@{host}:{port}/{DB_NAME}"
        print(f"Trying {host}:{port}...")
        try:
            engine = create_engine(url, connect_args={"sslmode": "require"}, connect_timeout=5)
            with engine.connect() as conn:
                print(f"  ✅ Connected to {host}")
                
                # Check stages
                res = conn.execute(text("SELECT COUNT(*) FROM stages"))
                count = res.scalar()
                
                if count == 0:
                    print("  Seeding stages...")
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
                    print(f"  ✅ Seeded {len(stages)} stages.")
                else:
                    print(f"  Stages already exist ({count} rows).")
                
                # Migration for projects
                print("  Running migrations...")
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS parent_record_id VARCHAR"))
                conn.execute(text("ALTER TABLE stage_history ADD COLUMN IF NOT EXISTS stage_status VARCHAR"))
                conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS can_add_users BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("  ✅ Migrations complete.")
                return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    return False

if __name__ == "__main__":
    fix()
