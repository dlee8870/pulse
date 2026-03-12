"""Database table definitions for raw posts and ingestion logs."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


def utcnow():
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class RawPost(Base):
    """A community post pulled from Reddit or loaded from seed data."""

    __tablename__ = "raw_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False, index=True)
    source_id = Column(String(255), nullable=False, unique=True)
    subreddit = Column(String(100), index=True)
    title = Column(Text, nullable=False)
    body = Column(Text, default="")
    author = Column(String(255))
    score = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    flair = Column(String(255))
    url = Column(Text)
    posted_at = Column(DateTime(timezone=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), default=utcnow)
    processed = Column(Boolean, default=False, index=True)


class IngestionLog(Base):
    """Tracks the result of a single ingestion run (fetched, new, duplicates, status)."""

    __tablename__ = "ingestion_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False)
    subreddit = Column(String(100))
    posts_fetched = Column(Integer, default=0)
    posts_new = Column(Integer, default=0)
    posts_duplicate = Column(Integer, default=0)
    status = Column(String(20), default="running")
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True), default=utcnow)
    completed_at = Column(DateTime(timezone=True))