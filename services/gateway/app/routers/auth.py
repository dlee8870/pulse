"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.dependencies import get_client_ip, get_current_user, get_redis
from app.models import ApiUser
from app.schemas import LoginRequest, TokenResponse, UserResponse
from app.security import create_access_token, verify_password
from app.services.rate_limiter import check_rate_limit

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
):
    """Authenticate a user and return a JWT access token."""
    client_ip = get_client_ip(http_request)
    rate_limit = await check_rate_limit(
        redis=redis,
        key=f"rate_limit:login:{client_ip}",
        limit=settings.login_rate_limit_requests,
        window_seconds=settings.login_rate_limit_window_seconds,
    )
    if not rate_limit.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts",
            headers={"Retry-After": str(rate_limit.retry_after_seconds)},
        )

    user = db.query(ApiUser).filter(ApiUser.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token, expires_in_seconds = create_access_token(str(user.id), user.username, settings)
    return TokenResponse(access_token=token, expires_in_seconds=expires_in_seconds)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: ApiUser = Depends(get_current_user)):
    """Return the authenticated user."""
    return current_user
