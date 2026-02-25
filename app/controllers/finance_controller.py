from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, engine, Base
from app.models.finance import ProjectFinancial, CostItem, Fund
from app.schemas import finance as schemas

router = APIRouter(prefix="/finance", tags=["finance"])

# Ensure tables exist at startup for this controller
@router.on_event("startup")
def init_finance_tables():
    Base.metadata.create_all(bind=engine)

@router.get("/financials", response_model=List[schemas.ProjectFinancial])
def get_financials(db: Session = Depends(get_db)):
    try:
        return db.query(ProjectFinancial).all()
    except Exception as e:
        print(f"Error fetching financials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/financials", response_model=schemas.ProjectFinancial)
def create_financial(financial: schemas.ProjectFinancialCreate, db: Session = Depends(get_db)):
    try:
        # Use .dict() for compatibility across Pydantic v1/v2
        data = financial.dict() if hasattr(financial, 'dict') else financial.model_dump()
        db_financial = ProjectFinancial(**data)
        db.add(db_financial)
        db.commit()
        db.refresh(db_financial)
        return db_financial
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/costs", response_model=List[schemas.CostItem])
def get_costs(db: Session = Depends(get_db)):
    try:
        return db.query(CostItem).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/costs", response_model=schemas.CostItem)
def create_cost(cost: schemas.CostItemCreate, db: Session = Depends(get_db)):
    try:
        data = cost.dict() if hasattr(cost, 'dict') else cost.model_dump()
        db_cost = CostItem(**data)
        db.add(db_cost)
        db.commit()
        db.refresh(db_cost)
        return db_cost
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/funds", response_model=List[schemas.Fund])
def get_funds(db: Session = Depends(get_db)):
    try:
        return db.query(Fund).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/funds", response_model=schemas.Fund)
def create_fund(fund: schemas.FundCreate, db: Session = Depends(get_db)):
    try:
        data = fund.dict() if hasattr(fund, 'dict') else fund.model_dump()
        db_fund = Fund(**data)
        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)
        return db_fund
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
