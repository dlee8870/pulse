"""Issue clustering and alert evaluation logic."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Alert, AlertRule, Issue, IssueEvent, IssuePost, ProcessedPost, RawPost

ALLOWED_TRANSITIONS = {
    "open": {"acknowledged", "resolved"},
    "acknowledged": {"investigating", "resolved"},
    "investigating": {"resolved"},
    "resolved": {"closed", "investigating"},
    "closed": set(),
}

ISSUE_TITLE_MAP = {
    ("gameplay-bug", "goalkeeper-logic"): "Goalkeeper AI and Positioning Issues",
    ("gameplay-bug", "fullback-tracking"): "Fullback Defensive Tracking Failures",
    ("gameplay-bug", "player-switching"): "Player Switching Inconsistency",
    ("gameplay-bug", "offside-logic"): "Offside Detection Inaccuracy",
    ("gameplay-bug", "auto-lunge"): "Unwanted Auto-Lunge Tackles",
    ("gameplay-bug", "first-touch"): "First Touch Quality Not Matching Stats",
    ("gameplay-bug", "passing-accuracy"): "Passing Goes to Wrong Player",
    ("gameplay-bug", "kickoff-goals"): "Kick-Off Goal Exploit",
    ("gameplay-bug", "referee-logic"): "Inconsistent Referee Decisions",
    ("gameplay-bug", "heading"): "Heading Accuracy Not Reflecting Stats",
    ("gameplay-bug", "corners"): "Corner Kick Balancing Issues",
    ("ui-bug", "sbc-interface"): "SBC Menu Filter Broken",
    ("ui-bug", "scoreboard-overlay"): "Scoreboard Overlay Stuck on Screen",
    ("ui-bug", "replay-camera"): "Goal Replay Showing Wrong Camera Angle",
    ("ui-bug", "companion-app"): "Companion App Crashes and Bugs",
    ("balance", "playstyle-dependency"): "PlayStyles Override Base Stats",
    ("balance", "pace-meta"): "Pace Dominates All Other Attributes",
    ("balance", "body-type"): "Body Type Matters More Than Ratings",
    ("balance", "ai-difficulty"): "AI Difficulty Scaling Feels Unfair",
    ("server-issue", "lag-delay"): "Server Lag and Input Delay",
    ("server-issue", "disconnection"): "Server Disconnections Causing Losses",
    ("feature-request", "skip-cutscenes"): "Add Option to Skip Celebrations and Replays",
    ("feature-request", "practice-mode"): "Add Proper Training and Practice Mode",
    ("feature-request", "career-mode"): "Career Mode Transfer Logic Overhaul",
    ("market", "price-crash"): "Transfer Market Price Instability",
    ("positive", "evolution-system"): "Evolution System Praise",
    ("positive", "chemistry-system"): "Chemistry System Praise",
    ("positive", "rush-mode"): "Rush Mode Praise",
    ("positive", "content-quality"): "Content Quality Praise",
}


def now_utc() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)


def derive_severity(avg_severity: float) -> str:
    """Map a numeric severity score to a human-readable label."""
    if avg_severity >= 0.85:
        return "critical"
    if avg_severity >= 0.65:
        return "high"
    if avg_severity >= 0.40:
        return "medium"
    return "low"


def build_issue_title(category: str, subcategory: str | None) -> str:
    """Look up a human-readable title, falling back to a formatted version."""
    key = (category, subcategory)
    if key in ISSUE_TITLE_MAP:
        return ISSUE_TITLE_MAP[key]

    label = subcategory or category
    return label.replace("-", " ").replace("_", " ").title()


def ensure_transition(current_status: str, next_status: str) -> bool:
    """Return True if the lifecycle transition is valid."""
    if current_status == next_status:
        return True
    return next_status in ALLOWED_TRANSITIONS.get(current_status, set())


def generate_issues(db: Session, min_posts: int, window_hours: int | None = None) -> list[Issue]:
    """Cluster unlinked processed posts by category/subcategory and create issues."""
    since = now_utc() - timedelta(hours=window_hours) if window_hours else None

    base_query = (
        db.query(
            ProcessedPost.category,
            ProcessedPost.subcategory,
            func.count(ProcessedPost.id).label("post_count"),
            func.avg(ProcessedPost.sentiment_score).label("avg_sentiment"),
            func.avg(ProcessedPost.severity_score).label("avg_severity"),
            func.min(RawPost.posted_at).label("first_reported"),
            func.max(RawPost.posted_at).label("last_activity"),
        )
        .join(RawPost, RawPost.id == ProcessedPost.raw_post_id)
        .outerjoin(IssuePost, IssuePost.processed_post_id == ProcessedPost.id)
        .filter(IssuePost.id.is_(None))
    )

    if since:
        base_query = base_query.filter(RawPost.posted_at >= since)

    clusters = (
        base_query
        .group_by(ProcessedPost.category, ProcessedPost.subcategory)
        .having(func.count(ProcessedPost.id) >= min_posts)
        .order_by(func.count(ProcessedPost.id).desc())
        .all()
    )

    created = []

    for cluster in clusters:
        category = cluster.category
        subcategory = cluster.subcategory
        avg_severity_value = float(cluster.avg_severity or 0.0)

        issue = Issue(
            title=build_issue_title(category, subcategory),
            description="Auto-generated from clustered community complaints.",
            category=category,
            subcategory=subcategory,
            status="open",
            severity=derive_severity(avg_severity_value),
            post_count=int(cluster.post_count),
            avg_sentiment=round(float(cluster.avg_sentiment or 0.0), 4),
            avg_severity=round(avg_severity_value, 4),
            first_reported_at=cluster.first_reported,
            last_activity_at=cluster.last_activity,
        )
        db.add(issue)
        db.flush()

        post_query = (
            db.query(ProcessedPost.id)
            .join(RawPost, RawPost.id == ProcessedPost.raw_post_id)
            .outerjoin(IssuePost, IssuePost.processed_post_id == ProcessedPost.id)
            .filter(ProcessedPost.category == category)
            .filter(ProcessedPost.subcategory == subcategory)
            .filter(IssuePost.id.is_(None))
        )

        if since:
            post_query = post_query.filter(RawPost.posted_at >= since)

        post_ids = post_query.all()

        for (processed_post_id,) in post_ids:
            db.add(IssuePost(issue_id=issue.id, processed_post_id=processed_post_id))

        window_label = f"the last {window_hours}h" if window_hours else "all time"
        db.add(
            IssueEvent(
                issue_id=issue.id,
                event_type="auto_created",
                message=f"Issue auto-created from {len(post_ids)} clustered posts ({window_label}).",
            )
        )
        created.append(issue)

    db.commit()

    for issue in created:
        db.refresh(issue)

    return created


def evaluate_alerts(db: Session) -> list[Alert]:
    """Check active rules against recent post counts and fire new alerts."""
    rules = db.query(AlertRule).filter(AlertRule.is_active == True).all()
    alerts = []

    for rule in rules:
        since = now_utc() - timedelta(hours=rule.time_window_hours)

        query = (
            db.query(func.count(ProcessedPost.id))
            .join(RawPost, RawPost.id == ProcessedPost.raw_post_id)
            .filter(RawPost.posted_at >= since)
            .filter(ProcessedPost.category == rule.category)
        )

        if rule.subcategory:
            query = query.filter(ProcessedPost.subcategory == rule.subcategory)

        current_count = int(query.scalar() or 0)
        if current_count < rule.threshold_count:
            continue

        already_fired = (
            db.query(Alert)
            .filter(Alert.rule_id == rule.id)
            .filter(Alert.triggered_at >= since)
            .first()
        )
        if already_fired:
            continue

        scope = f"{rule.category}/{rule.subcategory}" if rule.subcategory else rule.category
        alert = Alert(
            rule_id=rule.id,
            current_count=current_count,
            message=f"Rule '{rule.name}' triggered for {scope}: {current_count} posts in {rule.time_window_hours}h.",
        )
        db.add(alert)
        alerts.append(alert)

    db.commit()

    for alert in alerts:
        db.refresh(alert)

    return alerts