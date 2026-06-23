from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.assistant import ReplyRequest, ReplyOut
from app.models.lead import Lead
from app.models.product import Product
from app.services.llm_client import LLMClient, get_llm_client

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/reply", response_model=ReplyOut)
async def generate_reply(
    payload: ReplyRequest,
    db: Session = Depends(get_db),
    llm: LLMClient = Depends(get_llm_client),
):
    lead = db.query(Lead).get(payload.lead_id) if payload.lead_id else None
    products = []
    if payload.related_product_ids:
        products = (
            db.query(Product)
            .filter(Product.id.in_(payload.related_product_ids))
            .all()
        )

    context = {
        "lead": {
            "company_name": lead.company_name if lead else None,
            "industry": lead.industry if lead else None,
        } if lead else None,
        "products": [
            {"name": p.name, "description": p.description, "features": p.features}
            for p in products
        ],
        "message_from_client": payload.message_from_client,
    }

    reply_text = await llm.generate_reply(context)

    return ReplyOut(reply_text=reply_text)
