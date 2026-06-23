from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.offer import OfferGenerateRequest, OfferOut
from app.models.offer import Offer, OfferItem
from app.models.product import Product
from app.models.lead import Lead
from app.services.llm_client import LLMClient, get_llm_client

router = APIRouter(prefix="/offers", tags=["offers"])

@router.post("/generate", response_model=OfferOut)
async def generate_offer(
    payload: OfferGenerateRequest,
    db: Session = Depends(get_db),
    llm: LLMClient = Depends(get_llm_client),
):
    lead = db.query(Lead).get(payload.lead_id)
    product_ids = [i.product_id for i in payload.items]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    products_by_id = {p.id: p for p in products}

    total_price = 0
    currency = "PLN"
    offer_items = []

    for item in payload.items:
        product = products_by_id[item.product_id]
        unit_price = float(product.base_price)
        discount_percent = 0.0
        final_price = unit_price * item.quantity * (1 - discount_percent / 100)
        total_price += final_price

        offer_items.append(
            {
                "product_id": product.id,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "discount_percent": discount_percent,
                "final_price": final_price,
            }
        )

    llm_payload = {
        "lead": {
            "company_name": lead.company_name,
            "industry": lead.industry,
            "raw_message": lead.raw_message,
        },
        "items": [
            {
                "name": products_by_id[i["product_id"]].name,
                "description": products_by_id[i["product_id"]].description,
                "quantity": i["quantity"],
            }
            for i in offer_items
        ],
        "total_price": total_price,
        "currency": currency,
    }

    body_markdown = await llm.generate_offer_text(llm_payload)

    offer = Offer(
        lead_id=lead.id,
        title=f"Oferta dla {lead.company_name}",
        body_markdown=body_markdown,
        total_price=total_price,
        currency=currency,
        valid_until=datetime.utcnow() + timedelta(days=14),
        status="draft",
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    for i in offer_items:
        db.add(
            OfferItem(
                offer_id=offer.id,
                product_id=i["product_id"],
                quantity=i["quantity"],
                unit_price=i["unit_price"],
                discount_percent=i["discount_percent"],
                final_price=i["final_price"],
            )
        )
    db.commit()

    return OfferOut(
        id=offer.id,
        title=offer.title,
        body_markdown=offer.body_markdown,
        total_price=float(offer.total_price),
        currency=offer.currency,
    )
