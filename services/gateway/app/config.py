"""Gateway service configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings pulled from environment variables or .env file."""

    database_url: str = "postgresql://pulse:pulse_dev@localhost:5432/pulse"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "pulse_gateway_dev_secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_username: str = "pulse_admin"
    admin_password: str = "pulse_admin"
    proxy_timeout_seconds: float = 15.0
    login_rate_limit_requests: int = 5
    login_rate_limit_window_seconds: int = 60
    api_rate_limit_requests: int = 120
    api_rate_limit_window_seconds: int = 60
    ingestion_service_url: str = "http://ingestion:8000"
    processing_service_url: str = "http://processing:8000"
    analytics_service_url: str = "http://analytics:8000"
    issues_service_url: str = "http://issues:8000"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    model_config = {"env_file": ".env"}

    @property
    def cors_origin_list(self) -> list[str]:
        """Return configured CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
