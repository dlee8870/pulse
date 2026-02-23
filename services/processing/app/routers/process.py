import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProcessedPost, RawPost
from app.schemas import (
    BatchProcessRequest,
    BatchProcessResponse,
    CategoriesResponse,
    CategoryCount,
    PaginatedProcessedResponse,
    ProcessedPostDetail,
    ProcessedPostResponse,
    ProcessingStatusResponse,
)
from app.services.classifier import PostClassifier
from app.services.keyword_extractor import KeywordExtractor
from app.services.sentiment import SentimentAnalyzer
from app.services.severity import SeverityScorer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/process", tags=["Processing"])

analyzer = SentimentAnalyzer()
classifier = PostClassifier()
extractor = KeywordExtractor()
scorer = SeverityScorer()


@router.post("/batch", response_model=BatchProcessResponse)
def process_batch(
    request: BatchProcessRequest,
    db: Session = Depends(get_db),
):
    unprocessed = (
        db.query(RawPost)
        .filter(RawPost.processed == False)
        .limit(request.batch_size)
        .all()
    )

    if not unprocessed:
        total_remaining = (
            db.query(func.count(RawPost.id))
            .filter(RawPost.processed == False)
            .scalar()
        )
        return BatchProcessResponse(
            processed_count=0,
            skipped_count=0,
            total_remaining=total_remaining or 0,
            results=[],
        )

    results = []
    skipped = 0

    for raw_post in unprocessed:
        existing = (
            db.query(ProcessedPost)
            .filter(ProcessedPost.raw_post_id == raw_post.id)
            .first()
        )
        if existing:
            raw_post.processed = True
            skipped += 1
            continue

        combined_text = f"{raw_post.title} {raw_post.body or ''}"

        category, subcategory = classifier.classify(raw_post.title, raw_post.body, raw_post.flair)
        sentiment_score = analyzer.analyze(combined_text, category=category)
        keywords = extractor.extract(raw_post.title, raw_post.body)
        severity_score = scorer.score(
            sentiment_score=sentiment_score,
            post_score=raw_post.score,
            comment_count=raw_post.comment_count,
            category=category,
        )

        processed_post = ProcessedPost(
            raw_post_id=raw_post.id,
            category=category,
            subcategory=subcategory,
            sentiment_score=sentiment_score,
            severity_score=severity_score,
            keywords=keywords,
        )

        db.add(processed_post)
        raw_post.processed = True
        results.append(processed_post)

    db.commit()

    for result in results:
        db.refresh(result)

    total_remaining = (
        db.query(func.count(RawPost.id))
        .filter(RawPost.processed == False)
        .scalar()
    )

    logger.info(
        "Batch processing completed: %d processed, %d skipped, %d remaining",
        len(results),
        skipped,
        total_remaining,
    )

    return BatchProcessResponse(
        processed_count=len(results),
        skipped_count=skipped,
        total_remaining=total_remaining or 0,
        results=results,
    )


@router.get("/status", response_model=ProcessingStatusResponse)
def get_processing_status(db: Session = Depends(get_db)):
    total = db.query(func.count(RawPost.id)).scalar()
    processed = (
        db.query(func.count(RawPost.id))
        .filter(RawPost.processed == True)
        .scalar()
    )

    return ProcessingStatusResponse(
        total_posts=total or 0,
        processed=processed or 0,
        unprocessed=(total or 0) - (processed or 0),
    )


processed_router = APIRouter(prefix="/processed", tags=["Processed Posts"])


@processed_router.get("", response_model=PaginatedProcessedResponse)
def list_processed_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    category: str | None = None,
    subcategory: str | None = None,
    min_severity: float | None = Query(default=None, ge=0.0, le=1.0),
    max_severity: float | None = Query(default=None, ge=0.0, le=1.0),
    min_sentiment: float | None = Query(default=None, ge=-1.0, le=1.0),
    max_sentiment: float | None = Query(default=None, ge=-1.0, le=1.0),
    sort_by: str = Query(
        default="severity_score",
        pattern="^(severity_score|sentiment_score|processed_at)$",
    ),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            ProcessedPost.id,
            ProcessedPost.raw_post_id,
            ProcessedPost.category,
            ProcessedPost.subcategory,
            ProcessedPost.sentiment_score,
            ProcessedPost.severity_score,
            ProcessedPost.keywords,
            ProcessedPost.processed_at,
            RawPost.title,
            RawPost.body,
            RawPost.source,
            RawPost.subreddit,
            RawPost.score,
            RawPost.comment_count,
            RawPost.flair,
            RawPost.url,
            RawPost.posted_at,
        )
        .join(RawPost, ProcessedPost.raw_post_id == RawPost.id)
    )

    if category:
        query = query.filter(ProcessedPost.category == category)
    if subcategory:
        query = query.filter(ProcessedPost.subcategory == subcategory)
    if min_severity is not None:
        query = query.filter(ProcessedPost.severity_score >= min_severity)
    if max_severity is not None:
        query = query.filter(ProcessedPost.severity_score <= max_severity)
    if min_sentiment is not None:
        query = query.filter(ProcessedPost.sentiment_score >= min_sentiment)
    if max_sentiment is not None:
        query = query.filter(ProcessedPost.sentiment_score <= max_sentiment)

    total = query.count()

    sort_column = getattr(ProcessedPost, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    offset = (page - 1) * page_size
    rows = query.offset(offset).limit(page_size).all()
    total_pages = max(1, (total + page_size - 1) // page_size)

    items = [
        ProcessedPostDetail(
            id=row.id,
            raw_post_id=row.raw_post_id,
            category=row.category,
            subcategory=row.subcategory,
            sentiment_score=row.sentiment_score,
            severity_score=row.severity_score,
            keywords=row.keywords,
            processed_at=row.processed_at,
            title=row.title,
            body=row.body,
            source=row.source,
            subreddit=row.subreddit,
            score=row.score,
            comment_count=row.comment_count,
            flair=row.flair,
            url=row.url,
            posted_at=row.posted_at,
        )
        for row in rows
    ]

    return PaginatedProcessedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@processed_router.get("/{processed_id}", response_model=ProcessedPostDetail)
def get_processed_post(processed_id: UUID, db: Session = Depends(get_db)):
    row = (
        db.query(
            ProcessedPost.id,
            ProcessedPost.raw_post_id,
            ProcessedPost.category,
            ProcessedPost.subcategory,
            ProcessedPost.sentiment_score,
            ProcessedPost.severity_score,
            ProcessedPost.keywords,
            ProcessedPost.processed_at,
            RawPost.title,
            RawPost.body,
            RawPost.source,
            RawPost.subreddit,
            RawPost.score,
            RawPost.comment_count,
            RawPost.flair,
            RawPost.url,
            RawPost.posted_at,
        )
        .join(RawPost, ProcessedPost.raw_post_id == RawPost.id)
        .filter(ProcessedPost.id == processed_id)
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Processed post not found")

    return ProcessedPostDetail(
        id=row.id,
        raw_post_id=row.raw_post_id,
        category=row.category,
        subcategory=row.subcategory,
        sentiment_score=row.sentiment_score,
        severity_score=row.severity_score,
        keywords=row.keywords,
        processed_at=row.processed_at,
        title=row.title,
        body=row.body,
        source=row.source,
        subreddit=row.subreddit,
        score=row.score,
        comment_count=row.comment_count,
        flair=row.flair,
        url=row.url,
        posted_at=row.posted_at,
    )


categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("", response_model=CategoriesResponse)
def get_categories(db: Session = Depends(get_db)):
    counts = (
        db.query(
            ProcessedPost.category,
            ProcessedPost.subcategory,
            func.count(ProcessedPost.id),
        )
        .group_by(ProcessedPost.category, ProcessedPost.subcategory)
        .order_by(func.count(ProcessedPost.id).desc())
        .all()
    )

    total = db.query(func.count(ProcessedPost.id)).scalar()

    categories = [
        CategoryCount(category=cat, subcategory=sub, count=count)
        for cat, sub, count in counts
    ]

    return CategoriesResponse(
        categories=categories,
        total_processed=total or 0,
    )