import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.project import Project
from app.models.stage import Stage

def check():
    db = SessionLocal()
    db_path = None
    try:
        from app.database import DB_PATH
        db_path = DB_PATH
        print(f"Checking DB at: {db_path}")
    except ImportError:
        print("Using SQL database engine from config.")

    if db_path and not os.path.exists(db_path):
        print("LOCAL DB FILE NOT FOUND!")
        # If it's a local sqlite check, we might want to return. 
        # But if it's production, we continue with the engine check.

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
