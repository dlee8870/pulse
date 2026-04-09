"""Gateway service entry point."""

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import from_url

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import ApiUser
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.proxy import router as proxy_router
from app.security import hash_password

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def ensure_default_user() -> None:
    """Create the default gateway user when it does not exist."""
    settings = get_settings()
    db = SessionLocal()
    try:
        user = db.query(ApiUser).filter(ApiUser.username == settings.admin_username).first()
        if user is None:
            db.add(
                ApiUser(
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                    is_active=True,
                )
            )
            db.commit()
            logger.info("Created default gateway user '%s'", settings.admin_username)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create gateway resources on startup and close them on shutdown."""
    settings = get_settings()

    logger.info("Creating gateway tables...")
    Base.metadata.create_all(bind=engine)
    ensure_default_user()

    app.state.redis = from_url(settings.redis_url, decode_responses=True)
    app.state.http_client = httpx.AsyncClient()

    logger.info("Gateway service started")
    yield
    await app.state.http_client.aclose()
    await app.state.redis.aclose()
    logger.info("Gateway service shutting down")


settings = get_settings()

app = FastAPI(
    title="Pulse - API Gateway",
    description="Unified entry point for Pulse APIs with authentication, rate limiting, and service health checks.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(health_router)
app.include_router(proxy_router)
