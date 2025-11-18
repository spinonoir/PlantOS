"""Repository utilities for plants and related records."""
from __future__ import annotations

from typing import List, Optional

from plantos_backend.models import CareSignal, CareTask, Plant, TimelineEvent
from plantos_backend.schemas.plants import PlantCreate, PlantUpdate, TimelineEventCreate
from plantos_backend.storage.memory import memory_store


class PlantRepository:
    def list(self) -> List[Plant]:
        return sorted(memory_store.plants.values(), key=lambda plant: plant.created_at)

    def get(self, plant_id: str) -> Optional[Plant]:
        return memory_store.plants.get(plant_id)

    def create(self, payload: PlantCreate) -> Plant:
        plant = Plant(**payload.model_dump())
        memory_store.plants[plant.id] = plant
        for signal in (CareSignal.watering, CareSignal.feeding):
            task = CareTask.from_plant(plant, signal=signal)
            memory_store.care_tasks[task.id] = task
        return plant

    def update(self, plant_id: str, payload: PlantUpdate) -> Optional[Plant]:
        existing = memory_store.plants.get(plant_id)
        if not existing:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_data)
        memory_store.plants[plant_id] = updated
        return updated

    def delete(self, plant_id: str) -> bool:
        removed = memory_store.plants.pop(plant_id, None)
        if removed:
            tasks = [
                task_id
                for task_id, task in memory_store.care_tasks.items()
                if task.plant_id == plant_id
            ]
            for task_id in tasks:
                memory_store.care_tasks.pop(task_id, None)
            memory_store.timeline.pop(plant_id, None)
        return removed is not None

    def add_timeline_event(self, plant_id: str, payload: TimelineEventCreate) -> TimelineEvent:
        event = TimelineEvent(plant_id=plant_id, **payload.model_dump())
        memory_store.timeline.setdefault(plant_id, []).append(event)
        return event

    def list_timeline(self, plant_id: str) -> List[TimelineEvent]:
        return memory_store.timeline.get(plant_id, [])

    def list_tasks(self, plant_id: Optional[str] = None) -> List[CareTask]:
        tasks = list(memory_store.care_tasks.values())
        if plant_id:
            tasks = [task for task in tasks if task.plant_id == plant_id]
        return sorted(tasks, key=lambda task: task.next_due_at)


plant_repository = PlantRepository()
