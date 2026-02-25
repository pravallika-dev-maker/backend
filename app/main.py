from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.controllers import project_controller, stage_controller, resource_controller, history_controller, user_controller, finance_controller
from app.models import finance # Ensure models are loaded for create_all

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
                
                print("Migration: Checking/Adding access_level to users...")
                conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS access_level VARCHAR DEFAULT 'READ'"))

                print("Migration: Checking/Adding is_private to projects...")
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS is_private BOOLEAN DEFAULT FALSE"))
                
                print("Migration: Checking/Adding email to resources...")
                conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS email VARCHAR"))
                
                print("Migration: Checking/Adding access_level to resources...")
                conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS access_level VARCHAR DEFAULT 'READ'"))

                # Finance Module Migrations: Ensure all columns exist for funds, etc.
                print("Migration: Ensuring finance tables schema is correct...")
                # Funds Table — Add new columns if missing
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS investor_name VARCHAR"))
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS funding_date DATE"))
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS funding_type VARCHAR"))
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS notes TEXT"))

                # Rename old column 'amount' -> 'amount_raised' if it exists and new one doesn't
                try:
                    conn.execute(text("""
                        DO $$
                        BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='funds' AND column_name='amount')
                            AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='funds' AND column_name='amount_raised')
                            THEN
                                ALTER TABLE funds RENAME COLUMN amount TO amount_raised;
                            END IF;
                        END$$;
                    """))
                    print("Migration: Renamed 'amount' to 'amount_raised' in funds (if needed).")
                except Exception as e:
                    print(f"Migration note (amount rename): {e}")

                # Add amount_raised if still missing after rename attempt
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS amount_raised NUMERIC DEFAULT 0"))

                # Rename old column 'responsible_owner' -> 'owner_responsible' if it exists
                try:
                    conn.execute(text("""
                        DO $$
                        BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='funds' AND column_name='responsible_owner')
                            AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='funds' AND column_name='owner_responsible')
                            THEN
                                ALTER TABLE funds RENAME COLUMN responsible_owner TO owner_responsible;
                            END IF;
                        END$$;
                    """))
                    print("Migration: Renamed 'responsible_owner' to 'owner_responsible' in funds (if needed).")
                except Exception as e:
                    print(f"Migration note (responsible_owner rename): {e}")

                # Add owner_responsible if still missing after rename attempt
                conn.execute(text("ALTER TABLE funds ADD COLUMN IF NOT EXISTS owner_responsible VARCHAR"))

                # Project Financials
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS financial_id UUID PRIMARY KEY DEFAULT gen_random_uuid()"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS project_id VARCHAR"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS project_category VARCHAR"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS monthly_billing_amount NUMERIC DEFAULT 0"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS billing_owner VARCHAR"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS billing_start_date DATE"))
                conn.execute(text("ALTER TABLE project_financials ADD COLUMN IF NOT EXISTS billing_end_date DATE"))

                # Cost Items
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS cost_id UUID PRIMARY KEY DEFAULT gen_random_uuid()"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS cost_name VARCHAR"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS cost_category VARCHAR"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS monthly_amount NUMERIC DEFAULT 0"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS owner_name VARCHAR"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS start_date DATE"))
                conn.execute(text("ALTER TABLE cost_items ADD COLUMN IF NOT EXISTS end_date DATE"))

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

# CORS configuration - Robust Version
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://vrikshafrontend.vercel.app",
        "https://vriksha-command-center.vercel.app",
        "https://vrikshadashboard.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-User-Email", "Accept"],
)

# Include routers
app.include_router(project_controller.router)
app.include_router(stage_controller.router)
app.include_router(resource_controller.router)
app.include_router(history_controller.router)
app.include_router(user_controller.router)
app.include_router(finance_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dashboard API"}
