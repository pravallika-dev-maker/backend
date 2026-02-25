from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.finance import ProjectFinancial as PFModel, CostItem as CIModel, Fund as FundModel
from app.schemas.finance import ProjectFinancial, ProjectFinancialCreate, CostItem, CostItemCreate, Fund, FundCreate
from app.services.auth import get_current_user, require_ceo
from app.models.user import User as UserModel

router = APIRouter(
    prefix="/finance",
    tags=["finance"]
)

@router.get("/financials", response_model=List[ProjectFinancial])
def get_financials(db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    return db.query(PFModel).all()

@router.post("/financials", response_model=ProjectFinancial)
def create_financial(fin: ProjectFinancialCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    # Use model_dump() for Pydantic V2 compatibility
    db_fin = PFModel(**fin.model_dump())
    db.add(db_fin)
    db.commit()
    db.refresh(db_fin)
    return db_fin

@router.get("/costs", response_model=List[CostItem])
def get_costs(db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    return db.query(CIModel).all()

@router.post("/costs", response_model=CostItem)
def create_cost(cost: CostItemCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    # Use model_dump() for Pydantic V2 compatibility
    db_cost = CIModel(**cost.model_dump())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.get("/funds", response_model=List[Fund])
def get_funds(db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    return db.query(FundModel).all()

@router.post("/funds", response_model=Fund)
def create_fund(fund: FundCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    # Use model_dump() for Pydantic V2 compatibility
    db_fund = FundModel(**fund.model_dump())
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund
