from pydantic import BaseModel

class StageBase(BaseModel):
    stage_name: str
    stage_order: int

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
