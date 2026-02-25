from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

# =======================
# PROJECT FINANCIAL
# =======================

class ProjectFinancialBase(BaseModel):
    project_id: UUID   # ✅ FIX: must be UUID (not str)
    project_category: str
    monthly_billing_amount: float
    billing_owner: str
    billing_start_date: str
    billing_end_date: str


class ProjectFinancialCreate(ProjectFinancialBase):
    pass


class ProjectFinancial(ProjectFinancialBase):
    financial_id: UUID   # ✅ UUID from DB

    model_config = ConfigDict(from_attributes=True)


# =======================
# COST ITEM
# =======================

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
    cost_id: UUID

    model_config = ConfigDict(from_attributes=True)


# =======================
# FUND
# =======================

class FundBase(BaseModel):
    investor_name: str
    amount: float
    funding_date: str
    funding_type: str
    responsible_owner: str
    notes: Optional[str] = None


class FundCreate(FundBase):
    pass


class Fund(FundBase):
    fund_id: UUID

    model_config = ConfigDict(from_attributes=True)