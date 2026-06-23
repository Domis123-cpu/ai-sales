from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    company_name: str
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    raw_message: str
    source: Optional[str] = "web"

class LeadQualificationOut(BaseModel):
    score: int
    tier: str
    intent_summary: str
    budget_signal: str
    timeline_signal: str
    recommended_action: str

class LeadOut(BaseModel):
    id: int
    company_name: str
    contact_name: str
    email: EmailStr
    raw_message: str
    qualification: LeadQualificationOut

    class Config:
        from_attributes = True
