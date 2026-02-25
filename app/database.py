import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure we are in the 'backend' directory for the DB file
# Check env var first, otherwise default to Supabase
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")

# Fix for Railway/Heroku: SQLAlchemy requires postgresql://
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Supabase + Railway optimization:
# If using port 5432 (direct), it may fail on IPv6-only hosts. 
# Using the Supabase Pooler (port 6543) is highly recommended.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    # SSL is required for Supabase
    connect_args={"sslmode": "require"} if "supabase" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
