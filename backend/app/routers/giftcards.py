from app.core.database import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.redemption_service import RedemptionService
from app.schemas.giftcard import (
    GiftCardCreate, 
    GiftCardResponse, 
    GiftCardInfo, 
    RedemptionRequest, 
    RedemptionResponse
)


router = APIRouter(
    prefix="/giftcards",
    tags=["giftcards"]
)

@router.post("/issue", response_model=GiftCardResponse, status_code=status.HTTP_201_CREATED)
async def issue_gift_card(
    request: GiftCardCreate, 
    db: AsyncSession = Depends(get_db)
):
    code, gift_card = await RedemptionService.create_gift_card(db, request.initial_balance)
    
    return GiftCardResponse(
        code=code,
        initial_balance=gift_card.initial_balance,
        current_balance=gift_card.current_balance,
        status=gift_card.status,
        created_at=gift_card.created_at
    )

@router.get("/validate/{code}", response_model=GiftCardInfo)
async def validate_gift_card(
    code: str, 
    db: AsyncSession = Depends(get_db)
):
    gift_card = await RedemptionService.validate_gift_card(db, code)
    return GiftCardInfo(
        initial_balance=gift_card.initial_balance,
        current_balance=gift_card.current_balance,
        status=gift_card.status,
        created_at=gift_card.created_at
    )

@router.post("/redeem", response_model=RedemptionResponse)
async def redeem_gift_card(
    request: RedemptionRequest, 
    db: AsyncSession = Depends(get_db)
):
    redemption, new_balance = await RedemptionService.redeem_gift_card(
        db, 
        request.code, 
        request.amount,
        request.comment,
        request.idempotency_key
    )
    
    return RedemptionResponse(
        id=str(redemption.id),
        gift_card_id=str(redemption.gift_card_id),
        amount=redemption.amount,
        new_balance=new_balance,
        created_at=redemption.created_at
    )
