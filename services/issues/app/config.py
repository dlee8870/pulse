"""Issue service configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings pulled from environment variables or .env file."""

    database_url: str = "postgresql://pulse:pulse_dev@localhost:5432/pulse"
    redis_url: str = "redis://localhost:6379/0"
    auto_issue_min_posts: int = 1
    auto_issue_window_hours: int = 168

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()