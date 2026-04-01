"""Issue management endpoints."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.models import Issue, IssueEvent, IssuePost, ProcessedPost, RawPost
from app.schemas import (
    AutoGenerateRequest,
    AutoGenerateResponse,
    IssueCreateRequest,
    IssueDetailResponse,
    IssueEventResponse,
    IssuePatchRequest,
    IssuePostResponse,
    IssueResponse,
    PaginatedIssuesResponse,
)
from app.services.issue_engine import ensure_transition, generate_issues

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.get("", response_model=PaginatedIssuesResponse)
def list_issues(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: str | None = Query(default=None, pattern="^(open|acknowledged|investigating|resolved|closed)$"),
    severity: str | None = Query(default=None, pattern="^(low|medium|high|critical)$"),
    category: str | None = None,
    subcategory: str | None = None,
    db: Session = Depends(get_db),
):
    """Return a paginated list of issues with filters."""
    query = db.query(Issue)

    if status:
        query = query.filter(Issue.status == status)
    if severity:
        query = query.filter(Issue.severity == severity)
    if category:
        query = query.filter(Issue.category == category)
    if subcategory:
        query = query.filter(Issue.subcategory == subcategory)

    total = query.count()
    rows = (
        query.order_by(Issue.last_activity_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    total_pages = max(1, (total + page_size - 1) // page_size)

    return PaginatedIssuesResponse(
        items=rows,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("", response_model=IssueResponse, status_code=201)
def create_issue(request: IssueCreateRequest, db: Session = Depends(get_db)):
    """Create a manual issue."""
    current_time = datetime.now(timezone.utc)
    issue = Issue(
        title=request.title,
        description=request.description,
        category=request.category,
        subcategory=request.subcategory,
        status="open",
        severity=request.severity,
        post_count=0,
        avg_sentiment=0.0,
        avg_severity=0.0,
        first_reported_at=current_time,
        last_activity_at=current_time,
    )
    db.add(issue)
    db.flush()
    db.add(
        IssueEvent(
            issue_id=issue.id,
            event_type="manual_created",
            message="Issue created manually.",
        )
    )
    db.commit()
    db.refresh(issue)
    return issue


@router.get("/{issue_id}", response_model=IssueDetailResponse)
def get_issue(issue_id: UUID, db: Session = Depends(get_db)):
    """Return detailed issue data including timeline events."""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    timeline = (
        db.query(IssueEvent)
        .filter(IssueEvent.issue_id == issue_id)
        .order_by(IssueEvent.created_at.asc())
        .all()
    )

    return IssueDetailResponse.model_validate(
        {**IssueResponse.model_validate(issue).model_dump(), "timeline": timeline}
    )


@router.post("/auto-generate", response_model=AutoGenerateResponse)
def auto_generate_issues(
    request: AutoGenerateRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """Generate issues from clustered recent processed posts."""
    min_posts = request.min_posts if request.min_posts is not None else settings.auto_issue_min_posts
    window_hours = request.window_hours

    created = generate_issues(db, min_posts=min_posts, window_hours=window_hours)
    return AutoGenerateResponse(
        created_count=len(created),
        created_issue_ids=[issue.id for issue in created],
    )


@router.patch("/{issue_id}", response_model=IssueResponse)
def update_issue(issue_id: UUID, request: IssuePatchRequest, db: Session = Depends(get_db)):
    """Update issue lifecycle status, severity, or description."""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if request.status:
        if not ensure_transition(issue.status, request.status):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition: {issue.status} -> {request.status}",
            )
        if issue.status != request.status:
            db.add(
                IssueEvent(
                    issue_id=issue.id,
                    event_type="status_changed",
                    message=f"Status changed from {issue.status} to {request.status}.",
                )
            )
            issue.status = request.status

    if request.severity and issue.severity != request.severity:
        db.add(
            IssueEvent(
                issue_id=issue.id,
                event_type="severity_changed",
                message=f"Severity changed from {issue.severity} to {request.severity}.",
            )
        )
        issue.severity = request.severity

    if request.description is not None:
        issue.description = request.description

    db.commit()
    db.refresh(issue)
    return issue


@router.get("/{issue_id}/posts", response_model=list[IssuePostResponse])
def get_issue_posts(issue_id: UUID, db: Session = Depends(get_db)):
    """Return processed+raw posts linked to an issue."""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    rows = (
        db.query(
            ProcessedPost.id,
            ProcessedPost.raw_post_id,
            RawPost.title,
            RawPost.body,
            RawPost.source,
            RawPost.subreddit,
            RawPost.posted_at,
            ProcessedPost.category,
            ProcessedPost.subcategory,
            ProcessedPost.sentiment_score,
            ProcessedPost.severity_score,
        )
        .join(IssuePost, IssuePost.processed_post_id == ProcessedPost.id)
        .join(RawPost, RawPost.id == ProcessedPost.raw_post_id)
        .filter(IssuePost.issue_id == issue_id)
        .order_by(RawPost.posted_at.desc())
        .all()
    )

    return [
        IssuePostResponse(
            processed_post_id=row.id,
            raw_post_id=row.raw_post_id,
            title=row.title,
            body=row.body,
            source=row.source,
            subreddit=row.subreddit,
            posted_at=row.posted_at,
            category=row.category,
            subcategory=row.subcategory,
            sentiment_score=row.sentiment_score,
            severity_score=row.severity_score,
        )
        for row in rows
    ]