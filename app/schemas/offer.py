from pydantic import BaseModel
from typing import List

class OfferItemInput(BaseModel):
    product_id: int
    quantity: int

class OfferGenerateRequest(BaseModel):
    lead_id: int
    items: List[OfferItemInput]

class OfferOut(BaseModel):
    id: int
    title: str
    body_markdown: str
    total_price: float
    currency: str
