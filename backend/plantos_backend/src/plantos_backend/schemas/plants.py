"""Request/response schemas for plant endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from plantos_backend.models.plants import CareTask, LightLevel, Plant, TimelineEvent


class PlantCreate(BaseModel):
    name: str
    species: Optional[str] = None
    light_level: LightLevel = LightLevel.medium
    watering_interval_days: int = 7
    feeding_interval_days: int = 30
    reminders_enabled: bool = True
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    light_level: Optional[LightLevel] = None
    watering_interval_days: Optional[int] = None
    feeding_interval_days: Optional[int] = None
    reminders_enabled: Optional[bool] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class PlantResponse(Plant):
    pass


class CareTaskResponse(CareTask):
    pass


class TimelineEventCreate(BaseModel):
    event_type: str
    note: str
    photo_url: Optional[str] = None


class TimelineEventResponse(TimelineEvent):
    pass


class DueTask(BaseModel):
    task_id: str
    plant_id: str
    signal: str
    next_due_at: datetime
