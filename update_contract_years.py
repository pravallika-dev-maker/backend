import sys
import os
import random

# Ensure backend directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.project import Project

def update_and_display_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        # Common contract lengths to assign
        years_options = [1.0, 1.5, 2.0, 3.0, 5.0]
        
        updated_count = 0
        for p in projects:
            # We'll overwrite or set random duplicate years for the projects
            p.contract_years = random.choice(years_options)
            updated_count += 1
            
        db.commit()
        print(f"\n✅ Successfully updated {updated_count} projects with sample contract lengths!\n")
        
        print("=" * 80)
        print(f"{'RECORD ID':<12} | {'CLIENT NAME':<25} | {'DEAL STATUS':<12} | {'CONTRACT YRS'}")
        print("=" * 80)
        
        for p in projects:
            client = p.client_name[:24] if p.client_name else "Unknown"
            status = p.deal_status[:10] if p.deal_status else "N/A"
            years = f"{p.contract_years} Yrs" if p.contract_years else "N/A"
            print(f"{p.record_id:<12} | {client:<25} | {status:<12} | {years}")
            
        print("=" * 80)
            
    except Exception as e:
        db.rollback()
        print(f"Error updating projects: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_and_display_projects()
