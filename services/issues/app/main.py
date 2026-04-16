"""Issue service entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.error_handlers import register_exception_handlers
from app.models import Alert, AlertRule, Issue, IssueEvent, IssuePost, ProcessedPost, RawPost
from app.routers.alerts import router as alerts_router
from app.routers.issues import router as issues_router
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
    logger.info("Issue service started")
    yield
    logger.info("Issue service shutting down")


app = FastAPI(
    title="Pulse — Issue Management Service",
    description="Issue tracking and alerting built from clustered processed posts.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(issues_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Return service health status."""
    return HealthResponse(
        status="healthy",
        service="issues",
        version="1.0.0",
    )
