from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProcessedPostResponse(BaseModel):
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
    batch_size: int = 50


class BatchProcessResponse(BaseModel):
    processed_count: int
    skipped_count: int
    total_remaining: int
    results: list[ProcessedPostResponse]


class ProcessingStatusResponse(BaseModel):
    total_posts: int
    processed: int
    unprocessed: int


class PaginatedProcessedResponse(BaseModel):
    items: list[ProcessedPostDetail]
    total: int
    page: int
    page_size: int
    total_pages: int


class CategoryCount(BaseModel):
    category: str
    subcategory: str | None = None
    count: int


class CategoriesResponse(BaseModel):
    categories: list[CategoryCount]
    total_processed: int


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str