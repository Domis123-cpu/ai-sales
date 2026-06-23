from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadOut, LeadQualificationOut
from app.models.lead import Lead, LeadQualification
from app.services.llm_client import LLMClient, get_llm_client

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/ingest", response_model=LeadOut)
async def ingest_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
    llm: LLMClient = Depends(get_llm_client),
):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)

    llm_result = await llm.classify_lead(payload.model_dump())

    qual = LeadQualification(
        lead_id=lead.id,
        score=llm_result["score"],
        tier=llm_result["tier"],
        intent_summary=llm_result["intent_summary"],
        budget_signal=llm_result["budget_signal"],
        timeline_signal=llm_result["timeline_signal"],
        recommended_action=llm_result["recommended_action"],
        model_version="v1",
    )
    db.add(qual)
    db.commit()
    db.refresh(qual)

    qualification_out = LeadQualificationOut(
        score=qual.score,
        tier=qual.tier,
        intent_summary=qual.intent_summary,
        budget_signal=qual.budget_signal,
        timeline_signal=qual.timeline_signal,
        recommended_action=qual.recommended_action,
    )

    return LeadOut(
        id=lead.id,
        company_name=lead.company_name,
        contact_name=lead.contact_name,
        email=lead.email,
        raw_message=lead.raw_message,
        qualification=qualification_out,
    )
