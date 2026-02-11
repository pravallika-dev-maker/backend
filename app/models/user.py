from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True) # Set to nullable since we use Magic Links
    can_add_users = Column(Boolean, default=False) # True for CEO, False for others
    access_level = Column(String, default="READ") # "READ" or "WRITE"
