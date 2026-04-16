"""Tests for Redis-backed rate limiting."""

import asyncio

from redis.exceptions import RedisError

from app.services.rate_limiter import check_rate_limit


class FakeRedis:
    """Simple in-memory Redis double for rate-limit tests."""

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}
        self.ttls: dict[str, int] = {}

    async def incr(self, key: str) -> int:
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]

    async def expire(self, key: str, ttl: int) -> None:
        self.ttls[key] = ttl

    async def ttl(self, key: str) -> int:
        return self.ttls.get(key, -1)


class ExplodingRedis:
    """Redis double that simulates a backend failure."""

    async def incr(self, key: str) -> int:
        raise RedisError("boom")


def test_rate_limit_allows_request_within_limit() -> None:
    """Requests under the limit should be allowed."""
    redis = FakeRedis()

    result = asyncio.run(check_rate_limit(redis, "rate_limit:test", 5, 60))

    assert result.allowed is True
    assert result.limit == 5
    assert result.remaining == 4
    assert result.retry_after_seconds == 60


def test_rate_limit_blocks_when_limit_is_exceeded() -> None:
    """Requests above the limit should be rejected."""
    redis = FakeRedis()

    asyncio.run(check_rate_limit(redis, "rate_limit:test", 1, 60))
    result = asyncio.run(check_rate_limit(redis, "rate_limit:test", 1, 60))

    assert result.allowed is False
    assert result.remaining == 0
    assert result.retry_after_seconds == 60


def test_rate_limit_fails_open_when_redis_is_unavailable() -> None:
    """Redis failures should not block requests."""
    result = asyncio.run(check_rate_limit(ExplodingRedis(), "rate_limit:test", 10, 60))

    assert result.allowed is True
    assert result.limit == 10
    assert result.remaining == 9
    assert result.retry_after_seconds == 60
