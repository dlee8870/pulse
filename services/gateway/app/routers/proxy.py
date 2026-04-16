"""Authenticated proxy routes for backend services."""

from fastapi import APIRouter, Depends, Request
from httpx import AsyncClient
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.dependencies import get_current_user, get_http_client, get_redis
from app.models import ApiUser
from app.routers.proxy_helpers import proxy_service_request

router = APIRouter(prefix="/api", tags=["Gateway"])


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
    return await proxy_service_request(
        request=request,
        service_path=service_path,
        current_user=current_user,
        client=client,
        redis=redis,
        settings=settings,
    )
