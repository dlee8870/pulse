"""Helpers for forwarding requests to backend services."""

import httpx
from fastapi import HTTPException, Request, Response

from app.models import ApiUser

REQUEST_HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
    "authorization",
}

RESPONSE_HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
}


def _build_upstream_headers(request: Request, user: ApiUser) -> dict[str, str]:
    """Return request headers that are safe to forward upstream."""
    headers = {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in REQUEST_HOP_BY_HOP_HEADERS
    }
    headers["x-authenticated-user-id"] = str(user.id)
    headers["x-authenticated-username"] = user.username
    return headers


def _build_downstream_headers(response: httpx.Response) -> dict[str, str]:
    """Return response headers that are safe to return to the client."""
    return {
        name: value
        for name, value in response.headers.items()
        if name.lower() not in RESPONSE_HOP_BY_HOP_HEADERS
    }


async def forward_request(
    request: Request,
    http_client: httpx.AsyncClient,
    base_url: str,
    timeout_seconds: float,
    user: ApiUser,
) -> Response:
    """Forward the incoming request to an upstream service."""
    target_url = f"{base_url.rstrip('/')}{request.url.path}"
    headers = _build_upstream_headers(request, user)
    body = await request.body()

    try:
        upstream_response = await http_client.request(
            method=request.method,
            url=target_url,
            params=request.query_params,
            content=body,
            headers=headers,
            timeout=timeout_seconds,
        )
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Upstream service timed out") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="Upstream service unavailable") from exc

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=_build_downstream_headers(upstream_response),
    )
