"""Password hashing and JWT helpers."""

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

from app.config import Settings

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 600000


class AuthError(Exception):
    """Raised when a token cannot be validated."""


def hash_password(password: str) -> str:
    """Hash a password for storage."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    salt_b64 = base64.urlsafe_b64encode(salt).decode("utf-8")
    digest_b64 = base64.urlsafe_b64encode(digest).decode("utf-8")
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_b64}${digest_b64}"


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain password against a stored hash."""
    try:
        _, iterations, salt_b64, digest_b64 = password_hash.split("$")
    except ValueError:
        return False

    salt = base64.urlsafe_b64decode(salt_b64.encode("utf-8"))
    expected_digest = base64.urlsafe_b64decode(digest_b64.encode("utf-8"))
    actual_digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        int(iterations),
    )
    return hmac.compare_digest(actual_digest, expected_digest)


def create_access_token(user_id: str, username: str, settings: Settings) -> tuple[str, int]:
    """Create a signed access token for a user."""
    now = datetime.now(timezone.utc)
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_at = now + expires_delta
    payload = {
        "sub": user_id,
        "username": username,
        "type": "access",
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str, settings: Settings) -> dict:
    """Decode and validate an access token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except InvalidTokenError as exc:
        raise AuthError("Invalid token") from exc

    if payload.get("type") != "access":
        raise AuthError("Invalid token type")

    return payload
