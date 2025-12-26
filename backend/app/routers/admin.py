from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.redis import get_redis
from app.models.giftcard import GiftCard
from app.models.redemption import Redemption

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("/data")
async def get_all_data(db: AsyncSession = Depends(get_db)):
    # Fetch Gift Cards
    result_gc = await db.execute(select(GiftCard))
    gift_cards = result_gc.scalars().all()

    # Fetch Redemptions
    result_red = await db.execute(select(Redemption))
    redemptions = result_red.scalars().all()

    # Fetch Redis Data
    redis_client = await get_redis()
    try:
        keys = await redis_client.keys("*")
        redis_data = []
        if keys:
            values = await redis_client.mget(keys)
            for k, v in zip(keys, values):
                redis_data.append({"key": k, "value": v})
    finally:
        await redis_client.close()

    return {
        "gift_cards": [{c.name: getattr(gc, c.name) for c in gc.__table__.columns} for gc in gift_cards],
        "redemptions": [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in redemptions],
        "redis_data": redis_data
    }
