import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal
from backend.app.models.project import Project
from backend.app.models.stage import Stage

def check():
    db = SessionLocal()
    with open("db_status.txt", "w") as f:
        try:
            projects = db.query(Project).all()
            stages = db.query(Stage).all()
            
            f.write("=== DATABASE CHECK ===\n")
            f.write(f"Total Projects: {len(projects)}\n")
            f.write(f"Total Stages: {len(stages)}\n")
            
            if projects:
                f.write("\nSAMPLE PROJECTS:\n")
                for p in projects[:5]:
                    f.write(f"- Record ID: {p.record_id}\n")
                    f.write(f"  Client: {p.client_name}\n")
                    f.write(f"  Type: {p.deal_type}\n")
                    f.write(f"  Stage: {p.current_stage_name}\n")
                    f.write("---\n")
            else:
                f.write("\nNO PROJECTS FOUND IN DATABASE\n")
                
            if stages:
                f.write("\nSTAGES:\n")
                for s in stages:
                    f.write(f"- {s.stage_name} (Order: {s.stage_order})\n")
            else:
                f.write("\nNO STAGES FOUND IN DATABASE\n")
                
        except Exception as e:
            f.write(f"ERROR: {e}\n")
        finally:
            db.close()

if __name__ == "__main__":
    check()
