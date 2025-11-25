"""Application configuration powered by pydantic-settings."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Runtime configuration for PlantOS services."""

    app_name: str = "PlantOS Backend"
    api_version: str = "0.1.0"
    environment: str = "local"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    # AI Providers
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    default_ai_provider: str = "gemini"

    model_config = SettingsConfigDict(
        env_prefix="plantos_",
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
