"""Processing service entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.error_handlers import register_exception_handlers
from app.models import ProcessedPost, RawPost
from app.routers.process import categories_router, processed_router, router
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
    logger.info("Processing service started")
    yield
    logger.info("Processing service shutting down")


app = FastAPI(
    title="Pulse — Processing Service",
    description="NLP processing pipeline for community feedback. Classifies posts by category, analyzes sentiment, extracts keywords, and scores severity.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(router, prefix="/api")
app.include_router(processed_router, prefix="/api")
app.include_router(categories_router, prefix="/api")


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Return service health status."""
    return HealthResponse(
        status="healthy",
        service="processing",
        version="1.0.0",
    )
