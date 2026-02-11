from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String)
    role = Column(String)
    email = Column(String, nullable=True) # Link to user email
    access_level = Column(String, default="READ") # Per-project access level: READ or WRITE
    assigned_record_id = Column(String) # Linked to Project.record_id
