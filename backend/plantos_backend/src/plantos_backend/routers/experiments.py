"""Experiment API router."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from plantos_backend.services import experiments

router = APIRouter(prefix="/experiments", tags=["experiments"])


class CreateExperimentRequest(BaseModel):
    hypothesis: str
    metric_name: str
    variants: List[dict]


class LogMetricRequest(BaseModel):
    variant_id: str
    value: float


@router.get("", response_model=List[experiments.Experiment])
def list_experiments():
    return experiments.list_experiments()


@router.post("", response_model=experiments.Experiment, status_code=status.HTTP_201_CREATED)
def create_experiment(payload: CreateExperimentRequest):
    return experiments.create_experiment(
        payload.hypothesis,
        payload.metric_name,
        payload.variants
    )


@router.post("/{experiment_id}/metrics", response_model=experiments.Experiment)
def log_metric(experiment_id: str, payload: LogMetricRequest):
    experiment = experiments.log_metric(experiment_id, payload.variant_id, payload.value)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    return experiment


@router.post("/{experiment_id}/simulate", response_model=experiments.Experiment)
async def simulate_experiment(experiment_id: str):
    experiment = await experiments.simulate_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    return experiment
