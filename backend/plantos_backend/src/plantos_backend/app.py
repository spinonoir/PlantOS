"""FastAPI application factory for PlantOS."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from plantos_backend.routers import plants, schedules
from plantos_backend.settings import AppSettings, get_settings


def create_app(settings: AppSettings | None = None) -> FastAPI:
    current_settings = settings or get_settings()
    app = FastAPI(
        title=current_settings.app_name,
        version=current_settings.api_version,
        summary="PlantOS API surface",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=current_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(plants.router)
    app.include_router(schedules.router)

    return app


app = create_app()
