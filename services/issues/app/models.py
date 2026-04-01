"""Database models for issues and alerting."""

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
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


def utcnow():
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class ProcessedPost(Base):
    """Read-only mapping of processed_posts. Owned by the Processing Service."""

    __tablename__ = "processed_posts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    raw_post_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), index=True)
    sentiment_score = Column(Float, nullable=False)
    severity_score = Column(Float, nullable=False, index=True)
    processed_at = Column(DateTime(timezone=True), nullable=False)


class RawPost(Base):
    """Read-only mapping of raw_posts. Owned by the Ingestion Service."""

    __tablename__ = "raw_posts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(Text, nullable=False)
    body = Column(Text)
    source = Column(String(50), nullable=False)
    subreddit = Column(String(100), index=True)
    score = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    posted_at = Column(DateTime(timezone=True), nullable=False)


class Issue(Base):
    """A tracked community issue created from clusters of related posts."""

    __tablename__ = "issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), index=True)
    status = Column(String(20), nullable=False, default="open", index=True)
    severity = Column(String(20), nullable=False, default="medium", index=True)
    post_count = Column(Integer, nullable=False, default=0)
    avg_sentiment = Column(Float, nullable=False, default=0.0)
    avg_severity = Column(Float, nullable=False, default=0.0)
    first_reported_at = Column(DateTime(timezone=True), nullable=False)
    last_activity_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class IssuePost(Base):
    """Junction table linking a processed post to exactly one issue."""

    __tablename__ = "issue_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), nullable=False, index=True)
    processed_post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("processed_posts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    linked_at = Column(DateTime(timezone=True), default=utcnow)


class IssueEvent(Base):
    """Audit trail entry for issue lifecycle changes and automation events."""

    __tablename__ = "issue_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(30), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)


class AlertRule(Base):
    """Threshold-based rule that fires alerts when post volume exceeds a limit."""

    __tablename__ = "alert_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), index=True)
    threshold_count = Column(Integer, nullable=False)
    time_window_hours = Column(Integer, nullable=False)
    severity_level = Column(String(20), nullable=False, default="high")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)


class Alert(Base):
    """A triggered alert created when an active rule's threshold is exceeded."""

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    triggered_at = Column(DateTime(timezone=True), default=utcnow)
    current_count = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    acknowledged = Column(Boolean, nullable=False, default=False)