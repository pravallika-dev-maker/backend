from sqlalchemy import Column, Integer, String, Float, Date
from backend.app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, unique=True, index=True)
    client_name = Column(String)
    deal_type = Column(String)
    deal_value = Column(Float)
    project_owner_name = Column(String)
    current_stage_name = Column(String)
    next_stage_name = Column(String)
    next_stage_expected_date = Column(String)
    deal_status = Column(String)
    execution_status = Column(String)
    project_started_date = Column(String)
