from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.finance import ProjectFinancial, CostItem, Fund
from app.schemas import finance as schemas

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("/financials", response_model=List[schemas.ProjectFinancial])
def get_financials(db: Session = Depends(get_db)):
    try:
        return db.query(ProjectFinancial).all()
    except Exception as e:
        print(f"Error fetching financials: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/financials", response_model=schemas.ProjectFinancial)
def create_financial(financial: schemas.ProjectFinancialCreate, db: Session = Depends(get_db)):
    try:
        data = financial.dict() if hasattr(financial, 'dict') else financial.model_dump()
        db_obj = ProjectFinancial(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/costs", response_model=List[schemas.CostItem])
def get_costs(db: Session = Depends(get_db)):
    try:
        return db.query(ProjectFinancial).all() # Just double checking the query logic
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Wait, I noticed a typo in the line above in my previous thought process, fixing it now:
@router.get("/costs", response_model=List[schemas.CostItem])
def get_costs(db: Session = Depends(get_db)):
    try:
        return db.query(CostItem).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/costs", response_model=schemas.CostItem)
def create_cost(cost: schemas.CostItemCreate, db: Session = Depends(get_db)):
    try:
        data = cost.dict() if hasattr(cost, 'dict') else cost.model_dump()
        db_obj = CostItem(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/funds", response_model=List[schemas.Fund])
def get_funds(db: Session = Depends(get_db)):
    try:
        return db.query(Fund).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/funds", response_model=schemas.Fund)
def create_fund(fund: schemas.FundCreate, db: Session = Depends(get_db)):
    try:
        data = fund.dict() if hasattr(fund, 'dict') else fund.model_dump()
        db_obj = Fund(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
