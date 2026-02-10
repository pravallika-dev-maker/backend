from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.controllers import project_controller, stage_controller, resource_controller, history_controller, user_controller

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

# Migration: Ensure stage_status exists in stage_history
def run_migrations():
    # Only create tables and run migrations if we can connect
    try:
        print("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        
        with engine.connect() as conn:
            try:
                print("Migration: Checking/Adding stage_status to stage_history...")
                conn.execute(text("ALTER TABLE stage_history ADD COLUMN IF NOT EXISTS stage_status VARCHAR"))
                
                print("Migration: Checking/Adding can_add_users to users...")
                conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS can_add_users BOOLEAN DEFAULT FALSE"))
                
                print("Migration: Making hashed_password nullable in users...")
                # For SQLite, ALTER COLUMN is tricky, but for PostgreSQL:
                try:
                    conn.execute(text("ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL"))
                except Exception as e:
                    print(f"Note: Password nullability migration note (common in SQLite): {e}")

                try:
                    conn.commit()
                except:
                    pass
                print("Migration successful or already up to date.")
            except Exception as e:
                print(f"Inner migration failed: {e}")
    except Exception as e:
        print(f"Main migration or connection failed: {e}")

run_migrations()

app = FastAPI(
    title="Dashboard API",
    description="Backend for the Dashboard Project using FastAPI and MVC architecture",
    version="1.0.0"
)

import os

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if "*" not in origins:
    origins.extend([
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(project_controller.router)
app.include_router(stage_controller.router)
app.include_router(resource_controller.router)
app.include_router(history_controller.router)
app.include_router(user_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dashboard API"}
