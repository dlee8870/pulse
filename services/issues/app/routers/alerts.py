"""Alert rules and triggered alerts endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, AlertRule
from app.schemas import (
    AlertResponse,
    AlertRuleCreateRequest,
    AlertRuleResponse,
    EvaluateAlertsResponse,
)
from app.services.issue_engine import evaluate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])


# ---------------------------------------------------------------------------
# Alert Rules
# ---------------------------------------------------------------------------


@router.post("/rules", response_model=AlertRuleResponse, status_code=201)
def create_alert_rule(request: AlertRuleCreateRequest, db: Session = Depends(get_db)):
    """Create a new alert rule."""
    rule = AlertRule(
        name=request.name,
        category=request.category,
        subcategory=request.subcategory,
        threshold_count=request.threshold_count,
        time_window_hours=request.time_window_hours,
        severity_level=request.severity_level,
        is_active=request.is_active,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/rules", response_model=list[AlertRuleResponse])
def list_alert_rules(
    active_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    """Return alert rules, optionally filtered to active-only."""
    query = db.query(AlertRule)
    if active_only:
        query = query.filter(AlertRule.is_active == True)

    return query.order_by(AlertRule.created_at.desc()).all()


@router.patch("/rules/{rule_id}/toggle", response_model=AlertRuleResponse)
def toggle_rule(rule_id: UUID, db: Session = Depends(get_db)):
    """Enable or disable an alert rule."""
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    rule.is_active = not rule.is_active
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: UUID, db: Session = Depends(get_db)):
    """Delete an alert rule and all alerts it triggered."""
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    db.delete(rule)
    db.commit()


# ---------------------------------------------------------------------------
# Triggered Alerts
# ---------------------------------------------------------------------------


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    acknowledged: bool | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Return triggered alerts, newest first."""
    query = db.query(Alert)
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)

    return query.order_by(Alert.triggered_at.desc()).limit(limit).all()


@router.patch("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Mark a triggered alert as acknowledged."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert


@router.post("/evaluate", response_model=EvaluateAlertsResponse)
def trigger_alert_evaluation(db: Session = Depends(get_db)):
    """Evaluate all active alert rules against current post data."""
    alerts = evaluate_alerts(db)
    return EvaluateAlertsResponse(
        triggered_count=len(alerts),
        alert_ids=[alert.id for alert in alerts],
    )