from sqlalchemy import Column, String, Float, Date, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class ProjectFinancial(Base):
    __tablename__ = "project_financials"

    financial_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(String, index=True)
    project_category = Column(String)
    monthly_billing_amount = Column(Numeric)
    billing_owner = Column(String)
    billing_start_date = Column(Date)
    billing_end_date = Column(Date)

class CostItem(Base):
    __tablename__ = "cost_items"

    cost_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cost_name = Column(String)
    cost_category = Column(String)
    monthly_amount = Column(Numeric)
    owner_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

class Fund(Base):
    __tablename__ = "funds"

    # Changed from fund_id to id to match existing DB schema
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investor_name = Column(String)
    amount = Column(Numeric)
    funding_date = Column(Date)
    funding_type = Column(String)
    responsible_owner = Column(String)
    notes = Column(Text)
