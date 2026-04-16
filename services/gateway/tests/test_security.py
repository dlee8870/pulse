"""Tests for gateway authentication helpers."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.config import Settings
from app.security import AuthError, create_access_token, decode_access_token, hash_password, verify_password


def build_settings() -> Settings:
    """Return test settings with a stable secret."""
    return Settings(
        jwt_secret_key="test-secret",
        jwt_algorithm="HS256",
        access_token_expire_minutes=30,
    )


def test_hash_password_round_trip() -> None:
    """Hashed passwords should verify against the original plain value."""
    password_hash = hash_password("pulse-password")

    assert password_hash != "pulse-password"
    assert verify_password("pulse-password", password_hash) is True
    assert verify_password("wrong-password", password_hash) is False


def test_access_token_round_trip() -> None:
    """Created access tokens should decode to the same user payload."""
    settings = build_settings()

    token, expires_in_seconds = create_access_token("user-123", "pulse_admin", settings)
    payload = decode_access_token(token, settings)

    assert expires_in_seconds == 1800
    assert payload["sub"] == "user-123"
    assert payload["username"] == "pulse_admin"
    assert payload["type"] == "access"


def test_decode_access_token_rejects_wrong_token_type() -> None:
    """Non-access tokens should be rejected."""
    settings = build_settings()
    token = jwt.encode(
        {"sub": "user-123", "username": "pulse_admin", "type": "refresh"},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(AuthError):
        decode_access_token(token, settings)


def test_decode_access_token_rejects_expired_token() -> None:
    """Expired tokens should be rejected."""
    settings = build_settings()
    token = jwt.encode(
        {
            "sub": "user-123",
            "username": "pulse_admin",
            "type": "access",
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(AuthError):
        decode_access_token(token, settings)
