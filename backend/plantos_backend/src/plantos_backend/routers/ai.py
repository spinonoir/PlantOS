"""AI endpoints backed by LangGraph workflows."""
from __future__ import annotations

from fastapi import APIRouter

from plantos_backend.schemas.ai import (
    ExperimentReviewRequest,
    ExperimentReviewResponse,
    HealthCheckRequest,
    HealthCheckResponse,
    PlantIdentifyRequest,
    PlantIdentifyResponse,
)
from plantos_backend.services import ai

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/identify", response_model=PlantIdentifyResponse)
def identify_plant(payload: PlantIdentifyRequest) -> PlantIdentifyResponse:
    result = ai.run_onboarding(payload.photo_url, payload.notes)
    return PlantIdentifyResponse(**result)


@router.post("/health", response_model=HealthCheckResponse)
def diagnose(payload: HealthCheckRequest) -> HealthCheckResponse:
    result = ai.run_health_check(payload.description)
    return HealthCheckResponse(**result)


@router.post("/experiments/review", response_model=ExperimentReviewResponse)
def review_experiments(payload: ExperimentReviewRequest) -> ExperimentReviewResponse:
    result = ai.run_experiment_review(payload.model_dump())
    return ExperimentReviewResponse(**result)
