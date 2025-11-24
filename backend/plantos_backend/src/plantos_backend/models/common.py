"""Shared data structures for PlantOS domain models."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def generate_id(prefix: str) -> str:
    """Return a short, prefixed identifier for domain objects."""
    return f"{prefix}_{uuid4().hex[:8]}"


class TimestampedModel(BaseModel):
    """Base class that tracks creation and update timestamps."""

    id: str = Field(default_factory=lambda: generate_id("obj"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class Environment(str, Enum):
    local = "local"
    staging = "staging"
    production = "production"


class CareSignal(str, Enum):
    watering = "watering"
    feeding = "feeding"
    misting = "misting"
    pruning = "pruning"
    inspection = "inspection"


class ReminderChannel(str, Enum):
    push = "push"
    email = "email"
    sms = "sms"


Priority = Literal["low", "medium", "high"]


class CollectionNames(str, Enum):
    plants = "plants"
    tasks = "tasks"
    reminders = "reminders"
    events = "events"
    experiments = "experiments"

