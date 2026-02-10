from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.history import StageHistory as HistoryModel
from app.schemas.history import StageHistory, StageHistoryCreate
from app.services.auth import get_current_user, require_ceo
from app.models.user import User as UserModel

router = APIRouter(
    prefix="/history",
    tags=["history"]
)

@router.get("/{record_id}", response_model=List[StageHistory])
def read_history(record_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    try:
        history = db.query(HistoryModel).filter(HistoryModel.record_id == record_id).all()
        return history
    except Exception as e:
        error_msg = f"Failed to fetch history for {record_id}: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/", response_model=StageHistory)
def create_history_entry(entry: StageHistoryCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    db_entry = HistoryModel(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
