from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ProjectFinancial(Base):
    __tablename__ = "project_financials"

    id = Column("financial_id", Integer, primary_key=True, index=True)
    project_id = Column(String)
    project_category = Column(String)
    monthly_billing_amount = Column(Float)
    billing_owner = Column(String)
    billing_start_date = Column(String)
    billing_end_date = Column(String)

class CostItem(Base):
    __tablename__ = "cost_items"

    id = Column("cost_id", Integer, primary_key=True, index=True)
    cost_name = Column(String)
    cost_category = Column(String)
    monthly_amount = Column(Float)
    owner_name = Column(String)
    start_date = Column(String)
    end_date = Column(String)

class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    investor_name = Column(String)
    funding_amount = Column(Float)
    funding_date = Column(String)
    funding_type = Column(String)
    responsible_owner = Column(String)
    notes = Column(String)
