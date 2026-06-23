from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    budget = Column(Numeric(12, 2), nullable=True)
    timeline = Column(String, nullable=True)
    raw_message = Column(String, nullable=False)
    source = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    qualifications = relationship("LeadQualification", back_populates="lead")

class LeadQualification(Base):
    __tablename__ = "lead_qualification"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    score = Column(Integer, nullable=False)
    tier = Column(String, nullable=False)
    intent_summary = Column(String, nullable=False)
    budget_signal = Column(String, nullable=False)
    timeline_signal = Column(String, nullable=False)
    recommended_action = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="qualifications")
