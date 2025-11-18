"""Propagation batch tracking."""
from __future__ import annotations

from enum import Enum
from typing import Optional

from plantos_backend.models.common import TimestampedModel


class PropagationStage(str, Enum):
    cutting = "cutting"
    rooting = "rooting"
    acclimating = "acclimating"
    sale_ready = "sale_ready"


class PropagationBatch(TimestampedModel):
    mother_plant_id: str
    clone_count: int
    stage: PropagationStage = PropagationStage.cutting
    humidity: Optional[float] = None
    temperature: Optional[float] = None

    def mark_ready(self) -> None:
        self.stage = PropagationStage.sale_ready
