from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class ProjectFinancial(Base):
    __tablename__ = "project_financials"

    financial_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(String, index=True)
    project_category = Column(String)
    monthly_billing_amount = Column(Float)
    billing_owner = Column(String)
    billing_start_date = Column(String)
    billing_end_date = Column(String)

class CostItem(Base):
    __tablename__ = "cost_items"

    cost_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cost_name = Column(String)
    cost_category = Column(String)
    monthly_amount = Column(Float)
    owner_name = Column(String)
    start_date = Column(String)
    end_date = Column(String)

class Fund(Base):
    __tablename__ = "funds"

    fund_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investor_name = Column(String)
    amount = Column(Float)
    funding_date = Column(String)
    funding_type = Column(String)
    responsible_owner = Column(String)
    notes = Column(Text)
