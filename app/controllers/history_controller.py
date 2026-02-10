from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.history import StageHistory as HistoryModel
from app.schemas.history import StageHistory, StageHistoryCreate

router = APIRouter(
    prefix="/history",
    tags=["history"]
)

@router.get("/{record_id}", response_model=List[StageHistory])
def read_history(record_id: str, db: Session = Depends(get_db)):
    try:
        print(f"DEBUG: Fetching history for record_id: {record_id}")
        history = db.query(HistoryModel).filter(HistoryModel.record_id == record_id).all()
        print(f"DEBUG: Found {len(history)} history records")
        return history
    except Exception as e:
        error_msg = f"Failed to fetch history for {record_id}: {str(e)}"
        print(f"ERROR: {error_msg}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/", response_model=StageHistory)
def create_history_entry(entry: StageHistoryCreate, db: Session = Depends(get_db)):
    db_entry = HistoryModel(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
