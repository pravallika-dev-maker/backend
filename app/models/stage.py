from sqlalchemy import Column, Integer, String
from app.database import Base

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    stage_name = Column(String, unique=True, index=True)
    stage_order = Column(Integer)
