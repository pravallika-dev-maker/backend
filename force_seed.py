import os
import sys
import requests

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal, engine, Base
from backend.app.models.project import Project
from backend.app.models.stage import Stage
from backend.app.models.user import User

BASE_SHEET_URL = 'https://opensheet.elk.sh/1aqZD7MbMN_EJwnjVP6bBsXvt4NB0AN_Hk4LdNXFARP0'

def force_seed():
    print(f"Using database at: {engine.url}")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # User
        db.add(User(full_name="Admin", email="admin@example.com", hashed_password="password123"))
        
        # Projects
        print("Fetching projects from sheet...")
        resp = requests.get(f"{BASE_SHEET_URL}/Projects_Deals")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Found {len(data)} projects in sheet")
            for p in data:
                db_p = Project(
                    record_id=p.get('record_id'),
                    client_name=p.get('client_name'),
                    deal_type=p.get('deal_type'),
                    deal_value=float(str(p.get('deal_value', 0)).replace(',', '') or 0),
                    project_owner_name=p.get('project_owner_name'),
                    current_stage_name=p.get('current_stage_name'),
                    next_stage_name=p.get('next_stage_name'),
                    next_stage_expected_date=p.get('next_stage_expected_date')
                )
                db.add(db_p)
        else:
            print(f"Failed to fetch projects: {resp.status_code}")

        # Stages
        print("Fetching stages from sheet...")
        resp = requests.get(f"{BASE_SHEET_URL}/Stage_Master")
        if resp.status_code == 200:
            data = resp.json()
            for s in data:
                db.add(Stage(stage_name=s.get('stage_name'), stage_order=int(s.get('stage_order', 99))))

        db.commit()
        print("Force seed complete!")
        
        count = db.query(Project).count()
        print(f"Final project count in DB: {count}")
        
    except Exception as e:
        print(f"Error during force seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    force_seed()
