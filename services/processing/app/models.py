import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class RawPost(Base):
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


class ProcessedPost(Base):
    __tablename__ = "processed_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("raw_posts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), index=True)
    sentiment_score = Column(Float, nullable=False)
    severity_score = Column(Float, nullable=False, index=True)
    keywords = Column(JSON, default=list)
    processed_at = Column(DateTime(timezone=True), default=utcnow)