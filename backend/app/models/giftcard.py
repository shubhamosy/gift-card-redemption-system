import uuid
import enum
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float, DateTime, Enum


class GiftCardStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"


class GiftCard(Base):
    __tablename__ = "gift_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code_hash = Column(String, unique=True, index=True, nullable=False)
    initial_balance = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)
    status = Column(Enum(GiftCardStatus), default=GiftCardStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    redemptions = relationship("Redemption", back_populates="gift_card")
