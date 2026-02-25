from pydantic import BaseModel
from typing import Optional, List, Any

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
    financial_id: str 
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
    cost_id: str 
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
