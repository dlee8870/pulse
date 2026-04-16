"""Centralized exception handlers for the ingestion service."""

import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import ErrorResponse

logger = logging.getLogger(__name__)


def _build_error_response(
    request: Request,
    status_code: int,
    error: str,
    detail: object,
) -> JSONResponse:
    """Build a consistent error response payload."""
    payload = ErrorResponse(
        error=error,
        detail=detail,
        path=request.url.path,
        timestamp=datetime.now(timezone.utc),
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


def register_exception_handlers(app: FastAPI) -> None:
    """Register service-level exception handlers."""

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return _build_error_response(
            request=request,
            status_code=exc.status_code,
            error="http_error",
            detail=exc.detail,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _build_error_response(
            request=request,
            status_code=422,
            error="validation_error",
            detail=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception", exc_info=exc)
        return _build_error_response(
            request=request,
            status_code=500,
            error="internal_error",
            detail="Internal server error",
        )
