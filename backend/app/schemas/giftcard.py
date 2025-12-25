from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.giftcard import GiftCardStatus


class GiftCardCreate(BaseModel):
    initial_balance: float = Field(..., gt=0, description="Initial balance must be greater than 0")

class GiftCardResponse(BaseModel):
    code: str = Field(..., description="The plain text code (only shown once)")
    initial_balance: float
    current_balance: float
    status: GiftCardStatus
    created_at: datetime

class GiftCardInfo(BaseModel):
    initial_balance: float
    current_balance: float
    status: GiftCardStatus
    created_at: datetime

class RedemptionRequest(BaseModel):
    code: str = Field(..., min_length=12, max_length=12, description="12-character gift card code")
    amount: float = Field(..., gt=0, description="Amount to redeem")
    comment: Optional[str] = Field(None, description="Optional comment for the redemption")
    idempotency_key: Optional[str] = Field(None, description="Unique key to prevent duplicate transactions")

class RedemptionResponse(BaseModel):
    id: str
    gift_card_id: str
    amount: float
    new_balance: float
    status: str = "success"
    created_at: datetime
