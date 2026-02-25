from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import date

# =======================
# PROJECT FINANCIAL
# =======================

class ProjectFinancialBase(BaseModel):
    project_id: str
    project_category: str
    monthly_billing_amount: float
    billing_owner: str
    billing_start_date: date
    billing_end_date: date

class ProjectFinancialCreate(ProjectFinancialBase):
    pass

class ProjectFinancial(ProjectFinancialBase):
    financial_id: UUID

    model_config = ConfigDict(from_attributes=True)


# =======================
# COST ITEM
# =======================

class CostItemBase(BaseModel):
    cost_name: str
    cost_category: str
    monthly_amount: float
    owner_name: str
    start_date: date
    end_date: date

class CostItemCreate(CostItemBase):
    pass

class CostItem(CostItemBase):
    cost_id: UUID

    model_config = ConfigDict(from_attributes=True)


# =======================
# FUND
# =======================

class FundBase(BaseModel):
    investor_name: str
    amount: float
    funding_date: date
    funding_type: str
    responsible_owner: str
    notes: Optional[str] = None

class FundCreate(FundBase):
    pass

class Fund(FundBase):
    fund_id: UUID

    model_config = ConfigDict(from_attributes=True)