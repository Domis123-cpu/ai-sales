from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation, ConversationSummary
from app.schemas.conversation import ConversationCreate, ConversationSummaryOut
from app.services.llm_client import LLMClient, get_llm_client

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("", response_model=ConversationSummaryOut)
async def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    llm: LLMClient = Depends(get_llm_client),
):
    conv = Conversation(**payload.model_dump())
    db.add(conv)
    db.commit()
    db.refresh(conv)

    llm_result = await llm.summarize_conversation(payload.model_dump())

    summary = ConversationSummary(
        conversation_id=conv.id,
        summary=llm_result["summary"],
        key_needs=llm_result.get("key_needs"),
        objections=llm_result.get("objections"),
        next_steps=llm_result.get("next_steps"),
        estimated_potential=llm_result.get("estimated_potential"),
        model_version="v1",
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)

    return ConversationSummaryOut(
        summary=summary.summary,
        key_needs=summary.key_needs,
        objections=summary.objections,
        next_steps=summary.next_steps,
        estimated_potential=summary.estimated_potential,
    )
