"""In-memory data store used for prototypes and tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from plantos_backend.models import (
    CareTask,
    Experiment,
    Listing,
    Order,
    Plant,
    PropagationBatch,
    TimelineEvent,
)


@dataclass
class MemoryStore:
    plants: Dict[str, Plant] = field(default_factory=dict)
    care_tasks: Dict[str, CareTask] = field(default_factory=dict)
    timeline: Dict[str, List[TimelineEvent]] = field(default_factory=dict)
    experiments: Dict[str, Experiment] = field(default_factory=dict)
    propagations: Dict[str, PropagationBatch] = field(default_factory=dict)
    listings: Dict[str, Listing] = field(default_factory=dict)
    orders: Dict[str, Order] = field(default_factory=dict)


memory_store = MemoryStore()
