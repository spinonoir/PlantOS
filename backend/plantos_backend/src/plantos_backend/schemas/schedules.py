"""Schedule serialization."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from plantos_backend.schemas.plants import CareTaskResponse


class ScheduleDay(BaseModel):
    date: str
    tasks: List[CareTaskResponse]
