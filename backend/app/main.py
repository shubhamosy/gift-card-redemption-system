from fastapi import FastAPI
from app.routers import giftcards
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from app.models import giftcard, redemption
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error during startup: {e}")
    yield


app = FastAPI(
    title="Gift Card Redemption System",
    description="A secure backend for issuing, validating and redeeming gift cards.",
    version="1.2.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(giftcards.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gift Card Redemption System API"}
