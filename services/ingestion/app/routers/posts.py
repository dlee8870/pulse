"""Endpoints for querying and reading raw posts."""

import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RawPost
from app.schemas import PaginatedResponse, RawPostResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=PaginatedResponse)
def list_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    subreddit: str | None = None,
    processed: bool | None = None,
    min_score: int | None = None,
    search: str | None = None,
    sort_by: str = Query(default="ingested_at", pattern="^(ingested_at|posted_at|score|comment_count)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    posted_after: datetime | None = None,
    posted_before: datetime | None = None,
    db: Session = Depends(get_db),
):
    """Return a paginated list of raw posts with optional filters."""
    query = db.query(RawPost)

    if subreddit:
        query = query.filter(RawPost.subreddit == subreddit)
    if processed is not None:
        query = query.filter(RawPost.processed == processed)
    if min_score is not None:
        query = query.filter(RawPost.score >= min_score)
    if posted_after:
        query = query.filter(RawPost.posted_at >= posted_after)
    if posted_before:
        query = query.filter(RawPost.posted_at <= posted_before)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (RawPost.title.ilike(search_filter)) | (RawPost.body.ilike(search_filter))
        )

    total = query.count()

    sort_column = getattr(RawPost, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    offset = (page - 1) * page_size
    posts = query.offset(offset).limit(page_size).all()
    total_pages = max(1, (total + page_size - 1) // page_size)

    return PaginatedResponse(
        items=posts,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{post_id}", response_model=RawPostResponse)
def get_post(post_id: UUID, db: Session = Depends(get_db)):
    """Return a single raw post by ID."""
    post = db.query(RawPost).filter(RawPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/stats/summary")
def get_posts_summary(db: Session = Depends(get_db)):
    """Return aggregate stats: totals, processing status, average score, per-subreddit counts."""
    total = db.query(func.count(RawPost.id)).scalar()
    processed = (
        db.query(func.count(RawPost.id))
        .filter(RawPost.processed == True)
        .scalar()
    )
    unprocessed = total - processed

    subreddit_counts = (
        db.query(RawPost.subreddit, func.count(RawPost.id))
        .group_by(RawPost.subreddit)
        .all()
    )

    avg_score = db.query(func.avg(RawPost.score)).scalar()

    return {
        "total_posts": total,
        "processed": processed,
        "unprocessed": unprocessed,
        "average_score": round(float(avg_score), 1) if avg_score else 0,
        "by_subreddit": {name: count for name, count in subreddit_counts},
    }