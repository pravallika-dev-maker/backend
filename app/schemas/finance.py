from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date

class ProjectFinancialBase(BaseModel):
    project_id: str
    project_category: str
    monthly_billing_amount: float
    billing_owner: str
    billing_start_date: Any
    billing_end_date: Any

class ProjectFinancialCreate(ProjectFinancialBase):
    pass

class ProjectFinancial(ProjectFinancialBase):
    id: str # UUID from database
    class Config:
        from_attributes = True
        orm_mode = True

class CostItemBase(BaseModel):
    cost_name: str
    cost_category: str
    monthly_amount: float
    owner_name: str
    start_date: Any
    end_date: Any

class CostItemCreate(CostItemBase):
    pass

class CostItem(CostItemBase):
    id: str # UUID from database
    class Config:
        from_attributes = True
        orm_mode = True

class FundBase(BaseModel):
    investor_name: str
    funding_amount: float
    funding_date: Any
    funding_type: str
    responsible_owner: str
    notes: Optional[str] = None

class FundCreate(FundBase):
    pass

class Fund(FundBase):
    id: int
    class Config:
        from_attributes = True
        orm_mode = True

class FinanceSummary(BaseModel):
    financials: List[ProjectFinancial]
    costs: List[CostItem]
    funds: List[Fund]
