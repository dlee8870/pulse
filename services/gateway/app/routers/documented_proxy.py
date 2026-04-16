"""Swagger-friendly explicit proxy routes for key demo actions."""

from fastapi import APIRouter, Depends, Request, Response
from httpx import AsyncClient
from redis.asyncio import Redis

from app.config import Settings, get_settings
from app.dependencies import get_current_user, get_http_client, get_redis
from app.models import ApiUser
from app.routers.proxy_helpers import proxy_service_request
from app.schemas import (
    AutoGenerateIssueRequest,
    BatchProcessRequest,
    IngestSeedRequest,
    ProxyPassthroughResponse,
)

router = APIRouter(prefix="/api", tags=["Gateway"])


@router.post(
    "/ingest/seed",
    response_model=ProxyPassthroughResponse,
    summary="Seed demo posts",
)
async def seed_demo_posts(
    _payload: IngestSeedRequest,
    request: Request,
    current_user: ApiUser = Depends(get_current_user),
    client: AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> Response:
    """Forward the documented seed action to ingestion."""
    return await proxy_service_request(
        request=request,
        service_path="ingest/seed",
        current_user=current_user,
        client=client,
        redis=redis,
        settings=settings,
    )


@router.post(
    "/process/batch",
    response_model=ProxyPassthroughResponse,
    summary="Process a batch of posts",
)
async def process_batch(
    _payload: BatchProcessRequest,
    request: Request,
    current_user: ApiUser = Depends(get_current_user),
    client: AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> Response:
    """Forward the documented batch processing action to processing."""
    return await proxy_service_request(
        request=request,
        service_path="process/batch",
        current_user=current_user,
        client=client,
        redis=redis,
        settings=settings,
    )


@router.post(
    "/issues/auto-generate",
    response_model=ProxyPassthroughResponse,
    summary="Auto-generate issues",
)
async def auto_generate_issues(
    _payload: AutoGenerateIssueRequest,
    request: Request,
    current_user: ApiUser = Depends(get_current_user),
    client: AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> Response:
    """Forward the documented issue generation action to issues."""
    return await proxy_service_request(
        request=request,
        service_path="issues/auto-generate",
        current_user=current_user,
        client=client,
        redis=redis,
        settings=settings,
    )
