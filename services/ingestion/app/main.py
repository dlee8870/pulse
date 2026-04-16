"""Ingestion service entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.error_handlers import register_exception_handlers
from app.models import IngestionLog, RawPost
from app.routers import ingest, posts
from app.schemas import HealthResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup, log on shutdown."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Ingestion service started")
    yield
    logger.info("Ingestion service shutting down")


app = FastAPI(
    title="Pulse — Ingestion Service",
    description="Data ingestion pipeline for community feedback. Pulls posts from Reddit and other sources, normalizes them, and stores raw data for downstream processing.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(ingest.router, prefix="/api")
app.include_router(posts.router, prefix="/api")


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Return service health status."""
    return HealthResponse(
        status="healthy",
        service="ingestion",
        version="1.0.0",
    )
