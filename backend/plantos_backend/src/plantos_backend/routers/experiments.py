"""Experiment endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from plantos_backend.schemas.experiments import (
    ExperimentCreate,
    ExperimentMetricLog,
    ExperimentResponse,
)
from plantos_backend.services import ai
from plantos_backend.services import experiments as experiment_service

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
def create_experiment(payload: ExperimentCreate) -> ExperimentResponse:
    experiment = experiment_service.create_experiment(payload)
    ai.run_experiment_review(
        {"variants": [variant.model_dump() for variant in experiment.variants]}
    )
    return experiment


@router.get("", response_model=list[ExperimentResponse])
def list_experiments(plant_id: str | None = None) -> list[ExperimentResponse]:
    return experiment_service.list_experiments(plant_id)


@router.post("/{experiment_id}/metrics", response_model=ExperimentResponse)
def log_metric(experiment_id: str, payload: ExperimentMetricLog) -> ExperimentResponse:
    try:
        return experiment_service.log_metric(experiment_id, payload)
    except ValueError as exc:  # pragma: no cover - FastAPI handles response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
