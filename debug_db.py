from backend.app.database import SessionLocal
from backend.app.models.project import Project

db = SessionLocal()
projects = db.query(Project).all()
print(f"Total projects in DB: {len(projects)}")
for p in projects:
    print(f"ID: {p.record_id}, Client: {p.client_name}, Type: {p.deal_type}, Owner: {p.project_owner_name}")
db.close()
