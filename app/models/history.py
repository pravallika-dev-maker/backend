from sqlalchemy import Column, Integer, String
from app.database import Base

class StageHistory(Base):
    __tablename__ = "stage_history"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String)
    stage_name = Column(String)
    stage_start_date = Column(String)
    stage_end_date = Column(String)
    stage_status = Column(String)  # Completed, Skipped, In Progress
