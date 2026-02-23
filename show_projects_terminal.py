import sys
import os

# Ensure backend directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.project import Project

def display_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        print(f"Total Projects Built: {len(projects)}")
        print("=" * 80)
        for p in projects:
            print(f"  Record ID:        {p.record_id}")
            print(f"  Client Name:      {p.client_name}")
            print(f"  Deal Value:       ${p.deal_value:,.2f}" if p.deal_value is not None else "  Deal Value:       $0.00")
            print(f"  Project Owner:    {p.project_owner_name}")
            print(f"  Current Stage:    {p.current_stage_name}")
            print(f"  Status:           {p.deal_status} | {p.execution_status}")
            print(f"  Start Date:       {p.project_started_date}")
            if hasattr(p, 'contract_years'):
                print(f"  Contract Length:  {p.contract_years} Years" if p.contract_years else "  Contract Length:  N/A")
            print("-" * 80)
    finally:
        db.close()

if __name__ == "__main__":
    display_projects()
