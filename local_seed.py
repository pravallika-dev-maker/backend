import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.project import Project
from app.models.stage import Stage
from app.models.resource import Resource
from app.models.history import StageHistory
from app.models.user import User

def local_seed():
    print("Starting local seed...")
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed Admin User
        print("Seeding Admin User...")
        admin = User(
            full_name="Admin User",
            email="admin@example.com",
            hashed_password="password123"
        )
        db.add(admin)

        # Seed Stages
        print("Seeding Stages...")
        stage_names = ["Lead", "Contacted", "Proposal", "Negotiation", "Closing", "Execution"]
        for i, name in enumerate(stage_names):
            db.add(Stage(stage_name=name, stage_order=i+1))

        # Seed Projects
        print("Seeding Projects...")
        projects = [
            {
                "record_id": "REC001",
                "client_name": "Acme Corp",
                "deal_type": "Project",
                "deal_value": 50000.0,
                "project_owner_name": "John Doe",
                "current_stage_name": "Proposal",
                "next_stage_name": "Negotiation",
                "next_stage_expected_date": "2026-03-01",
                "deal_status": "Active",
                "execution_status": "Planning",
                "project_started_date": "2026-01-01"
            },
            {
                "record_id": "REC002",
                "client_name": "Globex",
                "deal_type": "Project",
                "deal_value": 75000.0,
                "project_owner_name": "Jane Smith",
                "current_stage_name": "Execution",
                "next_stage_name": "Closing",
                "next_stage_expected_date": "2026-04-15",
                "deal_status": "Active",
                "execution_status": "In Progress",
                "project_started_date": "2025-12-15"
            },
            {
                "record_id": "REC003",
                "client_name": "Soylent Corp",
                "deal_type": "Project",
                "deal_value": 25000.0,
                "project_owner_name": "Bob Brown",
                "current_stage_name": "Lead",
                "next_stage_name": "Contacted",
                "next_stage_expected_date": "2026-02-28",
                "deal_status": "Active",
                "execution_status": "New",
                "project_started_date": "2026-02-01"
            }
        ]
        
        for p_data in projects:
            db_p = Project(**p_data)
            db.add(db_p)

        db.commit()
        print("Local seed completed successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    local_seed()
