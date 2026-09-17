from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, JSON
from app.db.session import Base

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    complaint_number = Column(String(32), unique=True, nullable=False, index=True)
    complaint_source = Column(String(100), nullable=True)
    customer_name = Column(String(200), nullable=True)
    product_name = Column(String(200), nullable=True)
    product_strength = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True, index=True)
    affected_quantity = Column(String(100), nullable=True)
    manufacturing_date = Column(String(100), nullable=True)
    expiry_date = Column(String(100), nullable=True)
    originating_site = Column(String(100), nullable=True)
    impacted_materials = Column(String(300), nullable=True)
    complaint_category = Column(String(200), nullable=True)
    complaint_description = Column(Text, nullable=True)
    defect_summary = Column(Text, nullable=True)
    severity = Column(String(50), nullable=True)
    risk_level = Column(String(50), nullable=True)
    risk_score = Column(Float, nullable=True)
    risk_reasoning = Column(Text, nullable=True)
    suggested_action = Column(Text, nullable=True)
    capa_recommendation = Column(Text, nullable=True)
    completeness_score = Column(Float, nullable=True)
    missing_information = Column(JSON, nullable=True)
    source_text = Column(Text, nullable=True)
    status = Column(String(50), default="Pending Triage")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
