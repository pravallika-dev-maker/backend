from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.finance import ProjectFinancial, CostItem, Fund
from app.schemas import finance as schemas

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("/financials", response_model=List[schemas.ProjectFinancial])
def get_financials(db: Session = Depends(get_db)):
    return db.query(ProjectFinancial).all()

@router.post("/financials", response_model=schemas.ProjectFinancial)
def create_financial(financial: schemas.ProjectFinancialCreate, db: Session = Depends(get_db)):
    db_financial = ProjectFinancial(**financial.model_dump())
    db.add(db_financial)
    db.commit()
    db.refresh(db_financial)
    return db_financial

@router.get("/costs", response_model=List[schemas.CostItem])
def get_costs(db: Session = Depends(get_db)):
    return db.query(CostItem).all()

@router.post("/costs", response_model=schemas.CostItem)
def create_cost(cost: schemas.CostItemCreate, db: Session = Depends(get_db)):
    db_cost = CostItem(**cost.model_dump())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.get("/funds", response_model=List[schemas.Fund])
def get_funds(db: Session = Depends(get_db)):
    return db.query(Fund).all()

@router.post("/funds", response_model=schemas.Fund)
def create_fund(fund: schemas.FundCreate, db: Session = Depends(get_db)):
    db_fund = Fund(**fund.model_dump())
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund
