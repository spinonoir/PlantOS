"""Care schedule orchestration."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Iterable, List

from plantos_backend.models import CareSignal, CareTask, Plant


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


def calculate_conflict_free_window(
    task: CareTask, buffer_minutes: int = 10
) -> tuple[datetime, datetime]:
    start = task.next_due_at - timedelta(minutes=buffer_minutes)
    end = task.next_due_at + timedelta(minutes=buffer_minutes)
    return start, end
