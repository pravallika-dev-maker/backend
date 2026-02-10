from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.stage import Stage as StageModel
from app.schemas.stage import Stage, StageCreate

router = APIRouter(
    prefix="/stages",
    tags=["stages"]
)

@router.get("/", response_model=List[Stage])
def read_stages(db: Session = Depends(get_db)):
    stages = db.query(StageModel).order_by(StageModel.stage_order).all()
    return stages

@router.post("/", response_model=Stage)
def create_stage(stage: StageCreate, db: Session = Depends(get_db)):
    db_stage = StageModel(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage
