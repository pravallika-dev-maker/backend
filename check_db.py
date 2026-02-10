import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal
from backend.app.models.project import Project
from backend.app.models.stage import Stage

def check():
    db = SessionLocal()
    from backend.app.database import DB_PATH
    print(f"Checking DB at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("DB FILE NOT FOUND!")
        return

    try:
        projects = db.query(Project).all()
        stages = db.query(Stage).all()
        
        print("=== DATABASE CHECK ===")
        print(f"Total Projects: {len(projects)}")
        print(f"Total Stages: {len(stages)}")
        
        if projects:
            print("\nSAMPLE PROJECTS:")
            for p in projects[:5]:
                print(f"- Record ID: {p.record_id}")
                print(f"  Client: {p.client_name}")
                print(f"  Type: {p.deal_type}")
                print(f"  Stage: {p.current_stage_name}")
                print("---")
        else:
            print("\nNO PROJECTS FOUND IN DATABASE")
            
        if stages:
            print("\nSTAGES:")
            for s in stages:
                print(f"- {s.stage_name} (Order: {s.stage_order})")
        else:
            print("\nNO STAGES FOUND IN DATABASE")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check()
