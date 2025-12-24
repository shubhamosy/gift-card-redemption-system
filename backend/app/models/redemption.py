import uuid
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Float, ForeignKey, String


class Redemption(Base):
    __tablename__ = "redemptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gift_card_id = Column(UUID(as_uuid=True), ForeignKey("gift_cards.id"), nullable=False)
    amount = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    gift_card = relationship("GiftCard", back_populates="redemptions")
