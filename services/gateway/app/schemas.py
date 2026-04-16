"""Request and response schemas for the gateway."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class LoginRequest(BaseModel):
    """Credentials used to request an access token."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=128)


class TokenResponse(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int


class UserResponse(BaseModel):
    """Authenticated user response shape."""

    id: UUID
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class DependencyHealth(BaseModel):
    """Status for a single dependency or backend service."""

    name: str
    status: str
    detail: str | None = None


class GatewayHealthResponse(BaseModel):
    """Gateway health check response."""

    status: str
    service: str
    version: str
    dependencies: list[DependencyHealth]


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: str
    detail: Any
    path: str
    timestamp: datetime


class IngestSeedRequest(BaseModel):
    """Seed the demo dataset into the platform."""

    clear_existing: bool = Field(default=False)

    model_config = {"json_schema_extra": {"example": {"clear_existing": False}}}


class BatchProcessRequest(BaseModel):
    """Process a batch of raw posts."""

    batch_size: int = Field(default=50)

    model_config = {"json_schema_extra": {"example": {"batch_size": 50}}}


class AutoGenerateIssueRequest(BaseModel):
    """Generate issues from processed feedback."""

    min_posts: int | None = Field(default=None, ge=1, le=500)
    window_hours: int | None = Field(default=None, ge=1)

    model_config = {
        "json_schema_extra": {
            "example": {"min_posts": None, "window_hours": None}
        }
    }


class ProxyPassthroughResponse(RootModel[Any]):
    """Generic upstream response shape for documented proxy routes."""
