"""Request and response schemas for the ingestion API."""

from typing import Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RawPostResponse(BaseModel):
    """API response shape for a single raw post."""

    id: UUID
    source: str
    source_id: str
    subreddit: str | None = None
    title: str
    body: str | None = None
    author: str | None = None
    score: int = 0
    comment_count: int = 0
    flair: str | None = None
    url: str | None = None
    posted_at: datetime
    ingested_at: datetime
    processed: bool = False

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    """A page of posts with pagination metadata."""

    items: list[RawPostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class IngestRedditRequest(BaseModel):
    """Request body for triggering a live Reddit ingestion."""

    subreddits: list[str] = Field(default=["EAFC"], description="Subreddits to pull from")
    limit: int = Field(default=100, ge=1, le=500, description="Max posts per subreddit")
    sort: str = Field(default="hot", pattern="^(hot|new|top|rising)$")


class IngestSeedRequest(BaseModel):
    """Request body for loading seed data."""

    clear_existing: bool = Field(default=False, description="Remove all existing posts before seeding")


class IngestionLogResponse(BaseModel):
    """API response shape for an ingestion run log."""

    id: UUID
    source: str
    subreddit: str | None = None
    posts_fetched: int
    posts_new: int
    posts_duplicate: int
    status: str
    error_message: str | None = None
    started_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class IngestStatusResponse(BaseModel):
    """Overview of the ingestion system's current state."""

    last_run: IngestionLogResponse | None = None
    total_posts: int
    unprocessed_posts: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: str
    detail: Any
    path: str
    timestamp: datetime
