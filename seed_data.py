from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.project import Project
from app.models.stage import Stage
from app.models.resource import Resource
from app.models.history import StageHistory
from app.models.user import User

def seed():
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Seed User
    admin = User(
        full_name="Admin User",
        email="admin@example.com",
        hashed_password="password123"
    )
    db.add(admin)

    # Seed Stages
    stages = [
        Stage(stage_name="Lead", stage_order=1),
        Stage(stage_name="Contacted", stage_order=2),
        Stage(stage_name="Proposal", stage_order=3),
        Stage(stage_name="Negotiation", stage_order=4),
        Stage(stage_name="Closing", stage_order=5),
        Stage(stage_name="Execution", stage_order=6),
    ]
    for s in stages:
        db.add(s)

    # Seed Projects
    projects = [
        Project(
            record_id="PROJ001",
            client_name="Acme Corp",
            deal_type="Project",
            deal_value=500000,
            project_owner_name="John Doe",
            current_stage_name="Proposal",
            next_stage_name="Negotiation",
            next_stage_expected_date="2026-03-01",
            deal_status="Active",
            execution_status="In Progress",
            project_started_date="2026-01-15"
        ),
        Project(
            record_id="PROJ002",
            client_name="Global Tech",
            deal_type="Project",
            deal_value=1200000,
            project_owner_name="Jane Smith",
            current_stage_name="Execution",
            next_stage_name="Closing",
            next_stage_expected_date="2026-04-15",
            deal_status="Active",
            execution_status="On Track",
            project_started_date="2025-12-01"
        )
    ]
    for p in projects:
        db.add(p)

    # Seed Resources
    resources = [
        Resource(resource_name="Alice Wang", role="Frontend Developer", assigned_record_id="PROJ001"),
        Resource(resource_name="Bob Miller", role="Project Manager", assigned_record_id="PROJ001"),
        Resource(resource_name="Charlie Davis", role="Backend Lead", assigned_record_id="PROJ002"),
    ]
    for r in resources:
        db.add(r)

    # Seed History
    history = [
        StageHistory(record_id="PROJ001", stage_name="Lead", stage_start_date="2026-01-15", stage_end_date="2026-01-19"),
        StageHistory(record_id="PROJ001", stage_name="Contacted", stage_start_date="2026-01-20", stage_end_date="2026-01-31"),
        StageHistory(record_id="PROJ001", stage_name="Proposal", stage_start_date="2026-02-01", stage_end_date="2026-02-10"),
        StageHistory(record_id="PROJ002", stage_name="Lead", stage_start_date="2025-12-01", stage_end_date="2025-12-15"),
        StageHistory(record_id="PROJ002", stage_name="Execution", stage_start_date="2026-01-10", stage_end_date=""),
    ]
    for h in history:
        db.add(h)

    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
