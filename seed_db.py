import json
import requests
import sys
import os

# Add the project root to sys.path so 'backend' package can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.project import Project
from backend.app.models.stage import Stage
from backend.app.models.resource import Resource
from backend.app.models.history import StageHistory
from backend.app.models.user import User

BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

def seed_data():
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

        # Seed Projects
        print("Seeding Projects...")
        projects_data = requests.get(f"{BASE_SHEET_URL}/Projects_Deals").json()
        for p in projects_data:
            # Handle potential string to float conversion for deal_value
            deal_val = p.get('deal_value', 0)
            if isinstance(deal_val, str):
                deal_val = float(deal_val.replace(',', '') or 0)
            
            db_p = Project(
                record_id=p.get('record_id'),
                client_name=p.get('client_name'),
                deal_type=p.get('deal_type'),
                deal_value=deal_val,
                project_owner_name=p.get('project_owner_name'),
                current_stage_name=p.get('current_stage_name'),
                next_stage_name=p.get('next_stage_name'),
                next_stage_expected_date=p.get('next_stage_expected_date'),
                deal_status=p.get('deal_status', 'Active'),
                execution_status=p.get('execution_status', 'In Progress'),
                project_started_date=p.get('project_started_date', '2026-01-01')
            )
            db.add(db_p)

        # Seed Stages
        print("Seeding Stages...")
        stages_data = requests.get(f"{BASE_SHEET_URL}/Stage_Master").json()
        for s in stages_data:
            db_s = Stage(
                stage_name=s.get('stage_name'),
                stage_order=int(s.get('stage_order', 99))
            )
            db.add(db_s)

        # Seed Resources
        print("Seeding Resources...")
        resources_data = requests.get(f"{BASE_SHEET_URL}/Resources").json()
        for r in resources_data:
            db_r = Resource(
                resource_name=r.get('resource_name') or r.get('name'),
                role=r.get('role'),
                assigned_record_id=r.get('assigned_record_id')
            )
            db.add(db_r)

        # Seed History
        print("Seeding History...")
        history_data = requests.get(f"{BASE_SHEET_URL}/Stage_History").json()
        for h in history_data:
            db_h = StageHistory(
                record_id=h.get('record_id'),
                stage_name=h.get('stage_name'),
                stage_start_date=h.get('stage_start_date') or h.get('transition_date'),
                stage_end_date=h.get('stage_end_date') or h.get('transition_date')
            )
            db.add(db_h)

        db.commit()
        print("Seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
