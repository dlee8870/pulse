"""Request and response schemas for the processing API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProcessedPostResponse(BaseModel):
    """API response shape for NLP results only."""

    id: UUID
    raw_post_id: UUID
    category: str
    subcategory: str | None = None
    sentiment_score: float
    severity_score: float
    keywords: list[str] = []
    processed_at: datetime

    model_config = {"from_attributes": True}


class ProcessedPostDetail(BaseModel):
    """Full detail view: NLP results joined with original post data."""

    id: UUID
    raw_post_id: UUID
    category: str
    subcategory: str | None = None
    sentiment_score: float
    severity_score: float
    keywords: list[str] = []
    processed_at: datetime
    title: str
    body: str | None = None
    source: str
    subreddit: str | None = None
    score: int = 0
    comment_count: int = 0
    flair: str | None = None
    url: str | None = None
    posted_at: datetime

    model_config = {"from_attributes": True}


class BatchProcessRequest(BaseModel):
    """Request body for triggering batch processing."""

    batch_size: int = 50


class BatchProcessResponse(BaseModel):
    """Results from a batch processing run."""

    processed_count: int
    skipped_count: int
    total_remaining: int
    results: list[ProcessedPostResponse]


class ProcessingStatusResponse(BaseModel):
    """How many posts have been processed vs still pending."""

    total_posts: int
    processed: int
    unprocessed: int


class PaginatedProcessedResponse(BaseModel):
    """A page of processed posts with pagination metadata."""

    items: list[ProcessedPostDetail]
    total: int
    page: int
    page_size: int
    total_pages: int


class CategoryCount(BaseModel):
    """A category/subcategory pair with its post count."""

    category: str
    subcategory: str | None = None
    count: int


class CategoriesResponse(BaseModel):
    """Breakdown of all categories with counts."""

    categories: list[CategoryCount]
    total_processed: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str