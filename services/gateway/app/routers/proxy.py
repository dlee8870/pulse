"""Authenticated proxy routes for backend services."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from httpx import AsyncClient
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.dependencies import get_current_user, get_http_client, get_redis
from app.models import ApiUser
from app.services.proxy_client import forward_request
from app.services.rate_limiter import check_rate_limit

router = APIRouter(prefix="/api", tags=["Gateway"])


def resolve_service_url(service_path: str, settings: Settings) -> str:
    """Map an API path to the correct backend service."""
    root_segment = service_path.split("/", 1)[0]
    service_map = {
        "ingest": settings.ingestion_service_url,
        "posts": settings.ingestion_service_url,
        "process": settings.processing_service_url,
        "processed": settings.processing_service_url,
        "categories": settings.processing_service_url,
        "trends": settings.analytics_service_url,
        "rankings": settings.analytics_service_url,
        "patches": settings.analytics_service_url,
        "issues": settings.issues_service_url,
        "alerts": settings.issues_service_url,
    }
    target_url = service_map.get(root_segment)
    if not target_url:
        raise HTTPException(status_code=404, detail="Route not found")
    return target_url


@router.api_route(
    "/{service_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
async def proxy_request(
    request: Request,
    service_path: str,
    current_user: ApiUser = Depends(get_current_user),
    client: AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
):
    """Authenticate, rate-limit, and forward an API request."""
    rate_limit = await check_rate_limit(
        redis=redis,
        key=f"rate_limit:api:{current_user.id}",
        limit=settings.api_rate_limit_requests,
        window_seconds=settings.api_rate_limit_window_seconds,
    )
    if not rate_limit.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(rate_limit.retry_after_seconds)},
        )

    target_url = resolve_service_url(service_path, settings)
    return await forward_request(
        request=request,
        http_client=client,
        base_url=target_url,
        timeout_seconds=settings.proxy_timeout_seconds,
        user=current_user,
    )
