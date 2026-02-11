
from app.database import SessionLocal
from app.models.resource import Resource
from app.models.project import Project
from app.models.user import User

db = SessionLocal()

print("--- USERS ---")
users = db.query(User).all()
for u in users:
    print(f"User: {u.full_name}, Email: {u.email}, Role: {u.role}, Access: {u.access_level}, IS_CEO: {u.can_add_users}")

print("\n--- PROJECTS ---")
projects = db.query(Project).all()
for p in projects:
    print(f"Project: {p.client_name} (ID: {p.record_id})")
    
print("\n--- RESOURCES ---")
resources = db.query(Resource).all()
for r in resources:
    print(f"Resource: {r.resource_name}, Email: {r.email}, Role: {r.role}, Access: {r.access_level}, ProjectID: {r.assigned_record_id}")

db.close()
