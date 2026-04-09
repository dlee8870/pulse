"""Request and response schemas for the gateway."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


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
