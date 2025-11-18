"""Schemas for propagation APIs."""
from __future__ import annotations

from pydantic import BaseModel

from plantos_backend.models.propagation import PropagationBatch, PropagationStage


class PropagationCreate(BaseModel):
    mother_plant_id: str
    clone_count: int
    stage: PropagationStage = PropagationStage.cutting


class PropagationUpdate(BaseModel):
    stage: PropagationStage
    clone_count: int | None = None


class PropagationResponse(PropagationBatch):
    pass
