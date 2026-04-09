"""Gateway health check endpoints."""

import asyncio

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import text

from app.config import Settings, get_settings
from app.database import engine
from app.dependencies import get_http_client, get_redis
from app.schemas import DependencyHealth, GatewayHealthResponse

router = APIRouter(tags=["System"])


def _check_database() -> None:
    """Run a lightweight database check."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


async def _check_http_service(name: str, url: str, client: AsyncClient) -> DependencyHealth:
    """Check an upstream service health endpoint."""
    try:
        response = await client.get(f"{url.rstrip('/')}/health", timeout=5.0)
        if response.is_success:
            return DependencyHealth(name=name, status="healthy")
        return DependencyHealth(
            name=name,
            status="unhealthy",
            detail=f"Returned {response.status_code}",
        )
    except Exception as exc:
        return DependencyHealth(name=name, status="unhealthy", detail=str(exc))


async def _check_database_dependency() -> DependencyHealth:
    """Check database connectivity."""
    try:
        await asyncio.to_thread(_check_database)
        return DependencyHealth(name="postgres", status="healthy")
    except Exception as exc:
        return DependencyHealth(name="postgres", status="unhealthy", detail=str(exc))


async def _check_redis_dependency(redis: Redis) -> DependencyHealth:
    """Check Redis connectivity."""
    try:
        await redis.ping()
        return DependencyHealth(name="redis", status="healthy")
    except RedisError as exc:
        return DependencyHealth(name="redis", status="unhealthy", detail=str(exc))


@router.get("/health", response_model=GatewayHealthResponse)
async def health_check(
    request: Request,
    settings: Settings = Depends(get_settings),
    client: AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_redis),
):
    """Return gateway and dependency health status."""
    checks = await asyncio.gather(
        _check_database_dependency(),
        _check_redis_dependency(redis),
        _check_http_service("ingestion", settings.ingestion_service_url, client),
        _check_http_service("processing", settings.processing_service_url, client),
        _check_http_service("analytics", settings.analytics_service_url, client),
        _check_http_service("issues", settings.issues_service_url, client),
    )

    overall_status = "healthy" if all(item.status == "healthy" for item in checks) else "degraded"
    payload = GatewayHealthResponse(
        status=overall_status,
        service="gateway",
        version=request.app.version,
        dependencies=checks,
    )
    status_code = 200 if overall_status == "healthy" else 503
    return JSONResponse(status_code=status_code, content=payload.model_dump())
