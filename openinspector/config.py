from __future__ import annotations

import functools
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

ENV_PATH = Path(__file__).parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


class _Settings(BaseSettings):
    """Global configuration for OpenInspector loaded from env vars or .env file."""

    # Core service settings
    environment: str = Field("development", env="ENVIRONMENT")
    log_level: str = Field("info", env="LOG_LEVEL")
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    # OpenAI + LLM config
    openai_api_key: str = Field("", env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")

    # Database (sqlalchemy style url)
    database_url: str = Field("sqlite+aiosqlite:///openinspector.db", env="DATABASE_URL")

    # Tracing / LangSmith
    langsmith_project: Optional[str] = Field(None, env="LANGSMITH_PROJECT")

    # Security
    secret_key: str = Field("change-me", env="SECRET_KEY")

    class Config:
        case_sensitive = True
        env_file = str(ENV_PATH) if ENV_PATH.exists() else None
        env_file_encoding = "utf-8"


@functools.lru_cache(maxsize=1)
def _get_settings() -> _Settings:  # pragma: no cover
    return _Settings()


settings: _Settings = _get_settings() 