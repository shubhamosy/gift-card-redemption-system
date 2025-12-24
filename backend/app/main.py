from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import giftcard, redemption

app = FastAPI(title="Gift Card Redemption System")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
