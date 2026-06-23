from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    features = Column(JSON, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="PLN")
    segment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
