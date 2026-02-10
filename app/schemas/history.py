from pydantic import BaseModel
from typing import Optional

class StageHistoryBase(BaseModel):
    record_id: str
    stage_name: str
    stage_start_date: Optional[str] = None
    stage_end_date: Optional[str] = None
    stage_status: Optional[str] = None

class StageHistoryCreate(StageHistoryBase):
    pass

class StageHistory(StageHistoryBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
