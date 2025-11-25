"""Plant-centric data models."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import ClassVar, List, Optional


from pydantic import Field

from plantos_backend.models.common import CareSignal, CollectionNames, Priority, TimestampedModel, generate_id


class LightLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Plant(TimestampedModel):
    id: str = Field(default_factory=lambda: generate_id("plant"))
    name: str
    species: Optional[str] = None
    light_level: LightLevel = LightLevel.medium
    watering_interval_days: int = 7
    feeding_interval_days: int = 30
    reminders_enabled: bool = True
    tags: List[str] = Field(default_factory=list)

    collection_name: ClassVar[str] = CollectionNames.plants

    def next_watering_at(self, reference: datetime | None = None) -> datetime:
        reference_time = reference or datetime.now(timezone.utc)
        return reference_time + timedelta(days=self.watering_interval_days)


class CareTask(TimestampedModel):
    id: str = Field(default_factory=lambda: generate_id("task"))
    plant_id: str
    signal: CareSignal
    cadence_days: int
    next_due_at: datetime
    priority: Priority = "medium"
    duration_minutes: int = 5

    collection_name: ClassVar[str] = CollectionNames.tasks

    @classmethod
    def from_plant(cls, plant: Plant, signal: CareSignal) -> "CareTask":
        cadence = (
            plant.watering_interval_days
            if signal == CareSignal.watering
            else plant.feeding_interval_days
        )
        return cls(
            id=generate_id("task"),
            plant_id=plant.id,
            signal=signal,
            cadence_days=cadence,
            next_due_at=(
                plant.next_watering_at()
                if signal == CareSignal.watering
                else datetime.now(timezone.utc) + timedelta(days=cadence)
            ),
        )


class TimelineEvent(TimestampedModel):
    id: str = Field(default_factory=lambda: generate_id("event"))
    plant_id: str
    event_type: str
    note: str
    photo_url: Optional[str] = None

    collection_name: ClassVar[str] = CollectionNames.events



class Reminder(TimestampedModel):
    id: str = Field(default_factory=lambda: generate_id("reminder"))
    task_id: str
    send_at: datetime
    channel: str = "push"
    delivered_at: Optional[datetime] = None

    collection_name: ClassVar[str] = CollectionNames.reminders

