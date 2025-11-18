"""Meta and health endpoints."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from plantos_backend.settings import get_settings

router = APIRouter(prefix="", tags=["meta"])


@router.get("/health", summary="Health probe", description="Returns service readiness data.")
def read_health() -> dict[str, str]:
    settings = get_settings()
    timestamp = datetime.now(tz=timezone.utc).isoformat()
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.api_version,
        "environment": settings.environment,
        "timestamp": timestamp,
    }
