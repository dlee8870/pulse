"""Tests for Swagger-friendly documented proxy routes."""

import json
from types import SimpleNamespace
from uuid import uuid4

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.dependencies import get_current_user, get_http_client, get_redis
from app.routers.documented_proxy import router as documented_proxy_router
from app.routers.proxy import router as proxy_router


class FakeRedis:
    """Simple in-memory Redis double for route tests."""

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


class RecordingAsyncClient:
    """Minimal async HTTP client double that records proxied calls."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def request(self, **kwargs) -> httpx.Response:
        self.calls.append(kwargs)
        content = kwargs.get("content")
        body = json.loads(content.decode()) if content else None
        payload = {
            "url": str(kwargs["url"]),
            "method": kwargs["method"],
            "body": body,
        }
        return httpx.Response(
            status_code=202,
            json=payload,
            headers={"x-upstream-service": "ok"},
        )


def build_test_app(
    recording_client: RecordingAsyncClient,
    redis: FakeRedis,
    current_user: SimpleNamespace,
) -> FastAPI:
    """Build a lightweight app that mirrors gateway router registration."""
    app = FastAPI()
    app.include_router(documented_proxy_router)
    app.include_router(proxy_router)

    settings = Settings(
        ingestion_service_url="http://ingestion:8000",
        processing_service_url="http://processing:8000",
        analytics_service_url="http://analytics:8000",
        issues_service_url="http://issues:8000",
        api_rate_limit_requests=10,
        api_rate_limit_window_seconds=60,
        proxy_timeout_seconds=15.0,
    )
    app.dependency_overrides[get_current_user] = lambda: current_user
    app.dependency_overrides[get_http_client] = lambda: recording_client
    app.dependency_overrides[get_redis] = lambda: redis
    app.dependency_overrides[get_settings] = lambda: settings
    return app


def test_openapi_exposes_documented_request_bodies() -> None:
    """The explicit gateway routes should publish body schemas in OpenAPI."""
    app = build_test_app(
        recording_client=RecordingAsyncClient(),
        redis=FakeRedis(),
        current_user=SimpleNamespace(id=uuid4(), username="pulse_tester"),
    )

    schema = app.openapi()

    ingest_post = schema["paths"]["/api/ingest/seed"]["post"]
    process_post = schema["paths"]["/api/process/batch"]["post"]
    issues_post = schema["paths"]["/api/issues/auto-generate"]["post"]

    assert ingest_post["requestBody"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/IngestSeedRequest"
    )
    assert process_post["requestBody"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/BatchProcessRequest"
    )
    assert issues_post["requestBody"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/AutoGenerateIssueRequest"
    )
    assert schema["paths"]["/api/{service_path}"]["get"]["parameters"][0]["name"] == "service_path"


def test_explicit_seed_route_forwards_to_ingestion_service() -> None:
    """The documented seed route should proxy using the shared forwarding logic."""
    current_user = SimpleNamespace(id=uuid4(), username="pulse_tester")
    recording_client = RecordingAsyncClient()
    redis = FakeRedis()
    app = build_test_app(recording_client=recording_client, redis=redis, current_user=current_user)

    with TestClient(app) as client:
        response = client.post("/api/ingest/seed", json={"clear_existing": True})

    assert response.status_code == 202
    assert response.headers["x-upstream-service"] == "ok"
    assert response.json()["url"] == "http://ingestion:8000/api/ingest/seed"

    proxied_request = recording_client.calls[0]
    assert proxied_request["method"] == "POST"
    assert json.loads(proxied_request["content"].decode()) == {"clear_existing": True}
    assert proxied_request["headers"]["x-authenticated-username"] == "pulse_tester"
    assert "authorization" not in {
        header_name.lower() for header_name in proxied_request["headers"].keys()
    }
    assert redis.counts[f"rate_limit:api:{current_user.id}"] == 1


def test_catch_all_proxy_still_handles_undocumented_routes() -> None:
    """The generic proxy should continue handling routes without explicit docs."""
    recording_client = RecordingAsyncClient()
    app = build_test_app(
        recording_client=recording_client,
        redis=FakeRedis(),
        current_user=SimpleNamespace(id=uuid4(), username="pulse_tester"),
    )

    with TestClient(app) as client:
        response = client.get("/api/trends", params={"window_hours": 24})

    assert response.status_code == 202
    assert response.json()["url"] == "http://analytics:8000/api/trends"
    assert recording_client.calls[0]["params"]["window_hours"] == "24"
