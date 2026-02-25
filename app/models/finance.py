from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class ProjectFinancial(Base):
    __tablename__ = "project_financials"

    financial_id = Column(String, primary_key=True, index=True)
    project_id = Column(String)
    project_category = Column(String)
    monthly_billing_amount = Column(Float)
    billing_owner = Column(String)
    billing_start_date = Column(Date)
    billing_end_date = Column(Date)

class CostItem(Base):
    __tablename__ = "cost_items"

    cost_id = Column(String, primary_key=True, index=True)
    cost_name = Column(String)
    cost_category = Column(String)
    monthly_amount = Column(Float)
    owner_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    investor_name = Column(String)
    funding_amount = Column(Float)
    funding_date = Column(String) # Stored as text in setup script
    funding_type = Column(String)
    responsible_owner = Column(String)
    notes = Column(String)
