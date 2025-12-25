from fastapi import FastAPI
from app.routers import giftcards
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Gift Card Redemption System",
    description="A secure backend for issuing, validating and redeeming gift cards.",
    version="1.2.0",
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(giftcards.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gift Card Redemption System API"}
