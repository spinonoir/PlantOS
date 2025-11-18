"""Schemas for experiment APIs."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel

from plantos_backend.models.experiments import Experiment


class ExperimentVariantCreate(BaseModel):
    label: str
    description: str
    parameters: Dict[str, str] = {}


class ExperimentCreate(BaseModel):
    name: str
    hypothesis: str
    plant_id: str
    metric_keys: List[str]
    variants: List[ExperimentVariantCreate]


class ExperimentResponse(Experiment):
    pass


class ExperimentMetricLog(BaseModel):
    variant_id: str
    metric: str
    value: float


class ExperimentCompleteRequest(BaseModel):
    experiment_id: str
    winning_variant_id: str
