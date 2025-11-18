"""Experiment tracking models."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from pydantic import Field

from plantos_backend.models.common import TimestampedModel


class ExperimentVariant(TimestampedModel):
    label: str
    description: str
    parameters: Dict[str, str] = Field(default_factory=dict)
    metrics: Dict[str, float] = Field(default_factory=dict)


class Experiment(TimestampedModel):
    name: str
    hypothesis: str
    plant_id: str
    metric_keys: List[str]
    variants: List[ExperimentVariant]
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    metadata: Dict[str, str] = Field(default_factory=dict)

    def active(self) -> bool:
        return self.completed_at is None
