from fastapi import FastAPI
import logging
from app.routers import giftcards, admin
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from app.models import giftcard, redemption
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
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
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gift Card Redemption System API"}
