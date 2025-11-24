"""Care schedule orchestration."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Iterable, List

from plantos_backend.models import CareSignal, CareTask, Plant, TimelineEvent, CollectionNames
from datetime import timezone


def forecast_tasks(plants: Iterable[Plant], horizon_days: int = 7) -> List[CareTask]:
    """Generate care tasks for all plants within the time horizon."""
    tasks: List[CareTask] = []
    for plant in plants:
        for task in (
            CareTask.from_plant(plant, signal)
            for signal in (CareSignal.watering, CareSignal.feeding)
        ):
            window = datetime.now(task.next_due_at.tzinfo) + timedelta(days=horizon_days)
            if task.next_due_at <= window:
                tasks.append(task)
    return tasks


def merge_tasks(tasks: Iterable[CareTask]) -> Dict[str, List[CareTask]]:
    """Group tasks by due date (YYYY-MM-DD) to streamline notifications."""
    grouped: Dict[str, List[CareTask]] = defaultdict(list)
    for task in tasks:
        key = task.next_due_at.date().isoformat()
        grouped[key].append(task)
    return dict(grouped)


def generate_initial_tasks(plant: Plant) -> List[CareTask]:
    """Create initial care tasks for a new plant."""
    tasks = []
    # Watering
    tasks.append(CareTask.from_plant(plant, CareSignal.watering))
    # Feeding
    tasks.append(CareTask.from_plant(plant, CareSignal.feeding))
    return tasks


def complete_task(task: CareTask, plant: Plant) -> tuple[CareTask, TimelineEvent]:
    """
    Mark a task as complete.
    1. Create a completion event.
    2. Update the task's next_due_at based on the plant's interval.
    """
    # Create event
    event = TimelineEvent(
        plant_id=plant.id,
        event_type=f"{task.signal}_completed",
        note=f"Completed {task.signal} task",
    )

    # Calculate next due date
    # Ideally we use the completion time as the reference for the next interval
    # to avoid "drift" where you water late but the next one is still scheduled early.
    now = datetime.now(timezone.utc)
    
    if task.signal == CareSignal.watering:
        next_due = now + timedelta(days=plant.watering_interval_days)
    elif task.signal == CareSignal.feeding:
        next_due = now + timedelta(days=plant.feeding_interval_days)
    else:
        # Default fallback
        next_due = now + timedelta(days=7)

    updated_task = task.model_copy(update={"next_due_at": next_due})
    
    return updated_task, event

