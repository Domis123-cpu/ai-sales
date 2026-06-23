from pydantic import BaseModel
from typing import Optional, List

class ReplyRequest(BaseModel):
    lead_id: Optional[int] = None
    message_from_client: str
    related_product_ids: Optional[List[int]] = None

class ReplyOut(BaseModel):
    reply_text: str
