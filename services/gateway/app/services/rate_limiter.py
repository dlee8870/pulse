"""Redis-backed rate limiting helpers."""

import logging
from dataclasses import dataclass

from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RateLimitResult:
    """Result from evaluating a rate limit."""

    allowed: bool
    limit: int
    remaining: int
    retry_after_seconds: int


async def check_rate_limit(
    redis: Redis,
    key: str,
    limit: int,
    window_seconds: int,
) -> RateLimitResult:
    """Increment a fixed-window counter and report whether the request is allowed."""
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, window_seconds)

        ttl = await redis.ttl(key)
        retry_after_seconds = ttl if ttl > 0 else window_seconds
        allowed = count <= limit
        remaining = max(0, limit - count)

        return RateLimitResult(
            allowed=allowed,
            limit=limit,
            remaining=remaining,
            retry_after_seconds=retry_after_seconds,
        )
    except RedisError:
        logger.warning("Rate limiting unavailable; allowing request", exc_info=True)
        return RateLimitResult(
            allowed=True,
            limit=limit,
            remaining=max(0, limit - 1),
            retry_after_seconds=window_seconds,
        )
