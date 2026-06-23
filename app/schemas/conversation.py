from pydantic import BaseModel
from typing import Optional

class ConversationCreate(BaseModel):
    lead_id: Optional[int] = None
    channel: str
    raw_transcript: str

class ConversationSummaryOut(BaseModel):
    summary: str
    key_needs: Optional[str] = None
    objections: Optional[str] = None
    next_steps: Optional[str] = None
    estimated_potential: Optional[str] = None
