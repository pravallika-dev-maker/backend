from pydantic import BaseModel
from typing import Optional, List

class ProjectFinancialBase(BaseModel):
    project_id: str
    project_category: str
    monthly_billing_amount: float
    billing_owner: str
    billing_start_date: str
    billing_end_date: str

class ProjectFinancialCreate(ProjectFinancialBase):
    pass

class ProjectFinancial(ProjectFinancialBase):
    id: int
    class Config:
        # Support both Pydantic v1 and v2
        from_attributes = True
        orm_mode = True

class CostItemBase(BaseModel):
    cost_name: str
    cost_category: str
    monthly_amount: float
    owner_name: str
    start_date: str
    end_date: str

class CostItemCreate(CostItemBase):
    pass

class CostItem(CostItemBase):
    id: int
    class Config:
        from_attributes = True
        orm_mode = True

class FundBase(BaseModel):
    investor_name: str
    funding_amount: float
    funding_date: str
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
