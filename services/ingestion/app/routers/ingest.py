"""Endpoints for ingesting data from Reddit and seed files."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.models import IngestionLog, RawPost
from app.schemas import (
    IngestRedditRequest,
    IngestSeedRequest,
    IngestStatusResponse,
    IngestionLogResponse,
)
from app.services.reddit_client import RedditClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/reddit", response_model=IngestionLogResponse)
def trigger_reddit_ingestion(
    request: IngestRedditRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Fetch posts from Reddit and store new ones in the database."""
    if not settings.reddit_client_id or not settings.reddit_client_secret:
        raise HTTPException(
            status_code=400,
            detail="Reddit API credentials not configured. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env",
        )

    client = RedditClient(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    )

    log = IngestionLog(source="reddit", subreddit=",".join(request.subreddits))
    db.add(log)
    db.commit()

    total_fetched = 0
    total_new = 0
    total_duplicate = 0

    try:
        for subreddit_name in request.subreddits:
            posts = client.fetch_posts(
                subreddit=subreddit_name,
                sort=request.sort,
                limit=request.limit,
            )
            total_fetched += len(posts)

            for post_data in posts:
                existing = (
                    db.query(RawPost)
                    .filter(RawPost.source_id == post_data["source_id"])
                    .first()
                )
                if existing:
                    total_duplicate += 1
                    continue

                raw_post = RawPost(**post_data)
                db.add(raw_post)
                total_new += 1

            db.commit()

        log.posts_fetched = total_fetched
        log.posts_new = total_new
        log.posts_duplicate = total_duplicate
        log.status = "completed"
        log.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(log)

        logger.info(
            "Reddit ingestion completed: %d fetched, %d new, %d duplicates",
            total_fetched,
            total_new,
            total_duplicate,
        )
        return log

    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.now(timezone.utc)
        db.commit()
        logger.error("Reddit ingestion failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}") from e


@router.post("/seed", response_model=IngestionLogResponse)
def trigger_seed_ingestion(
    request: IngestSeedRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Load seed data from a local JSON file into the database."""
    seed_path = Path(settings.seed_data_path)
    if not seed_path.exists():
        raise HTTPException(status_code=404, detail=f"Seed data not found at {seed_path}")

    log = IngestionLog(source="seed", subreddit="seed_data")
    db.add(log)
    db.commit()

    try:
        if request.clear_existing:
            db.query(RawPost).filter(RawPost.source == "seed").delete()
            db.commit()

        with open(seed_path) as f:
            seed_posts = json.load(f)

        total_fetched = len(seed_posts)
        total_new = 0
        total_duplicate = 0

        for post_data in seed_posts:
            existing = (
                db.query(RawPost)
                .filter(RawPost.source_id == post_data["source_id"])
                .first()
            )
            if existing:
                total_duplicate += 1
                continue

            post_data["posted_at"] = datetime.fromisoformat(post_data["posted_at"])
            raw_post = RawPost(**post_data)
            db.add(raw_post)
            total_new += 1

        db.commit()

        log.posts_fetched = total_fetched
        log.posts_new = total_new
        log.posts_duplicate = total_duplicate
        log.status = "completed"
        log.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(log)

        logger.info("Seed ingestion completed: %d new posts loaded", total_new)
        return log

    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.now(timezone.utc)
        db.commit()
        logger.error("Seed ingestion failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Seed ingestion failed: {e}") from e


@router.get("/status", response_model=IngestStatusResponse)
def get_ingestion_status(db: Session = Depends(get_db)):
    """Return the last ingestion run and current post counts."""
    last_run = (
        db.query(IngestionLog)
        .order_by(IngestionLog.started_at.desc())
        .first()
    )
    total_posts = db.query(func.count(RawPost.id)).scalar()
    unprocessed_posts = (
        db.query(func.count(RawPost.id))
        .filter(RawPost.processed == False)
        .scalar()
    )

    return IngestStatusResponse(
        last_run=last_run,
        total_posts=total_posts,
        unprocessed_posts=unprocessed_posts,
    )


@router.get("/logs", response_model=list[IngestionLogResponse])
def get_ingestion_logs(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Return recent ingestion logs, newest first."""
    logs = (
        db.query(IngestionLog)
        .order_by(IngestionLog.started_at.desc())
        .limit(limit)
        .all()
    )
    return logs