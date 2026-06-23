from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    channel = Column(String, nullable=False)
    raw_transcript = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    summaries = relationship("ConversationSummary", back_populates="conversation")

class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    summary = Column(String, nullable=False)
    key_needs = Column(String, nullable=True)
    objections = Column(String, nullable=True)
    next_steps = Column(String, nullable=True)
    estimated_potential = Column(String, nullable=True)
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="summaries")
