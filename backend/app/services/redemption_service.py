import string
import secrets
from sqlalchemy import select
from fastapi import HTTPException
from app.core.redis import get_redis
from sqlalchemy.exc import IntegrityError
from app.core.security import get_code_hash
from app.models.redemption import Redemption
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.giftcard import GiftCard, GiftCardStatus


class RedemptionService:
    @staticmethod
    def generate_code(length=12) -> str:
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))


    @staticmethod
    async def create_gift_card(db: AsyncSession, initial_balance: float) -> tuple[str, GiftCard]:
        code = RedemptionService.generate_code()
        code_hash = get_code_hash(code)
        
        gift_card = GiftCard(
            code_hash=code_hash,
            initial_balance=initial_balance,
            current_balance=initial_balance,
            status=GiftCardStatus.ACTIVE
        )
        
        db.add(gift_card)
        try:
            await db.commit()
            await db.refresh(gift_card)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error generating unique card code")
            
        return code, gift_card

    @staticmethod
    async def validate_gift_card(db: AsyncSession, code: str) -> GiftCard:
        code_hash = get_code_hash(code) 
        result = await db.execute(select(GiftCard).where(GiftCard.code_hash == code_hash))
        gift_card = result.scalars().first()
        
        if not gift_card:
            raise HTTPException(status_code=404, detail="Gift card not found")
            
        if gift_card.status != GiftCardStatus.ACTIVE:
            raise HTTPException(status_code=400, detail=f"Gift card is {gift_card.status}")
            
        return gift_card

    @staticmethod
    async def redeem_gift_card(
        db: AsyncSession, 
        code: str, 
        amount: float,
        comment: str = None,
        idempotency_key: str = None
    ) -> tuple[Redemption, float]:
        
        # 1. Idempotency Check
        redis_client = await get_redis()
        if idempotency_key:
            cached_result = await redis_client.get(f"redemption:{idempotency_key}")
            if cached_result:
                raise HTTPException(status_code=409, detail="Transaction already processed")
                
        # 2. Validate Card & Lock Row
        code_hash = get_code_hash(code)

        query = select(GiftCard).where(GiftCard.code_hash == code_hash).with_for_update()
        result = await db.execute(query)
        gift_card = result.scalars().first()
        
        if not gift_card:
            raise HTTPException(status_code=404, detail="Gift card not found")
            
        if gift_card.status != GiftCardStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Gift card is inactive")
            
        if gift_card.current_balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
            
        # 3. Execute Redemption
        gift_card.current_balance -= amount
        
        redemption = Redemption(
            gift_card_id=gift_card.id,
            amount=amount,
            comment=comment
        )
        db.add(redemption)
        
        await db.commit()
        await db.refresh(redemption)
        
        # 4. Set Idempotency Key
        if idempotency_key:
            await redis_client.set(f"redemption:{idempotency_key}", str(redemption.id), ex=3600)
            
        return redemption, gift_card.current_balance
