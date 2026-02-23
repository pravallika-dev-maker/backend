import sys
import os
import random

# Ensure backend directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.project import Project

def update_categories():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        categories = ["Services", "Marketing", "Product"]
        
        updated_count = 0
        for p in projects:
            p.project_category = random.choice(categories)
            updated_count += 1
            
        db.commit()
        print(f"\n✅ Successfully updated {updated_count} projects with random categories!\n")
        
        print("=" * 100)
        print(f"{'RECORD ID':<12} | {'CLIENT NAME':<25} | {'STATUS':<12} | {'YRS':<5} | {'CATEGORY'}")
        print("=" * 100)
        
        for p in projects:
            client = p.client_name[:24] if p.client_name else "Unknown"
            status = p.deal_status[:10] if p.deal_status else "N/A"
            years = f"{p.contract_years}" if p.contract_years else "N/A"
            category = p.project_category if p.project_category else "N/A"
            print(f"{p.record_id:<12} | {client:<25} | {status:<12} | {years:<5} | {category}")
            
        print("=" * 100)
            
    except Exception as e:
        db.rollback()
        print(f"Error updating projects: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_categories()
