"""Request and response schemas for issue management."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IssueBase(BaseModel):
    """Shared issue fields."""

    title: str
    description: str | None = None
    category: str
    subcategory: str | None = None
    severity: str = Field(default="medium", pattern="^(low|medium|high|critical)$")


class IssueCreateRequest(IssueBase):
    """Request body for creating a manual issue."""


class IssuePatchRequest(BaseModel):
    """Request body for updating issue status, severity, or description."""

    status: str | None = Field(default=None, pattern="^(open|acknowledged|investigating|resolved|closed)$")
    severity: str | None = Field(default=None, pattern="^(low|medium|high|critical)$")
    description: str | None = None


class IssueResponse(IssueBase):
    """Issue response shape."""

    id: UUID
    status: str
    post_count: int
    avg_sentiment: float
    avg_severity: float
    first_reported_at: datetime
    last_activity_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IssueEventResponse(BaseModel):
    """Timeline event response shape."""

    id: UUID
    issue_id: UUID
    event_type: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


class IssueDetailResponse(IssueResponse):
    """Detailed issue response including full audit timeline."""

    timeline: list[IssueEventResponse]


class IssuePostResponse(BaseModel):
    """A processed post linked to an issue, joined with original post data."""

    processed_post_id: UUID
    raw_post_id: UUID
    title: str
    body: str | None = None
    source: str
    subreddit: str | None = None
    posted_at: datetime
    category: str
    subcategory: str | None = None
    sentiment_score: float
    severity_score: float


class PaginatedIssuesResponse(BaseModel):
    """A page of issues with pagination metadata."""

    items: list[IssueResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AutoGenerateRequest(BaseModel):
    """Parameters for automatic issue generation. Omit fields to use config defaults."""

    min_posts: int | None = Field(default=None, ge=1, le=500)
    window_hours: int | None = Field(default=None, ge=1)


class AutoGenerateResponse(BaseModel):
    """Result of an auto-generation run."""

    created_count: int
    created_issue_ids: list[UUID]


class AlertRuleCreateRequest(BaseModel):
    """Request body for creating an alert rule."""

    name: str
    category: str
    subcategory: str | None = None
    threshold_count: int = Field(ge=1)
    time_window_hours: int = Field(ge=1)
    severity_level: str = Field(default="high", pattern="^(low|medium|high|critical)$")
    is_active: bool = True


class AlertRuleResponse(BaseModel):
    """Alert rule response shape."""

    id: UUID
    name: str
    category: str
    subcategory: str | None = None
    threshold_count: int
    time_window_hours: int
    severity_level: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertResponse(BaseModel):
    """Triggered alert response shape."""

    id: UUID
    rule_id: UUID
    triggered_at: datetime
    current_count: int
    message: str
    acknowledged: bool

    model_config = {"from_attributes": True}


class EvaluateAlertsResponse(BaseModel):
    """Result from evaluating active alert rules."""

    triggered_count: int
    alert_ids: list[UUID]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str