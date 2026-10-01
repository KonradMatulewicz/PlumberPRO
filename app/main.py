"""FastAPI application entry point (composition root)."""

from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()
app = FastAPI(title="DataOps Copilot", version=settings.app_version)


@app.get("/health", tags=["platform"])
def health() -> dict[str, str]:
    """Health endpoint pattern: used by Render, smoke tests and monitoring.

    US-01: extend with a real DB connectivity check (status 'degraded' when DB unreachable).
    """
    return {"status": "ok", "version": settings.app_version, "env": settings.app_env}
