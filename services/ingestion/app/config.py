"""Ingestion service configuration."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings pulled from environment variables or .env file."""

    database_url: str = "postgresql://pulse:pulse_dev@localhost:5432/pulse"
    redis_url: str = "redis://localhost:6379/0"
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "Pulse/1.0 (Community Intelligence Platform)"
    default_subreddits: list[str] = ["EAFC", "FIFA"]
    default_fetch_limit: int = 100
    seed_data_path: str = "/app/data/seed_posts.json"

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()