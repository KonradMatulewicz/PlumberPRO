"""Runtime configuration from environment variables (12-factor). No secrets in code."""

import os
from dataclasses import dataclass, field


def _flag(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "dev"))
    app_version: str = field(default_factory=lambda: os.getenv("APP_VERSION", "0.1.0"))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    ingest_api_key: str = field(default_factory=lambda: os.getenv("INGEST_API_KEY", ""))
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "fake"))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", ""))
    embeddings_provider: str = field(default_factory=lambda: os.getenv("EMBEDDINGS_PROVIDER", "tfidf"))
    feature_copilot: bool = field(default_factory=lambda: _flag("FEATURE_COPILOT", True))
    feature_risk_model: bool = field(default_factory=lambda: _flag("FEATURE_RISK_MODEL", True))


def get_settings() -> Settings:
    return Settings()
