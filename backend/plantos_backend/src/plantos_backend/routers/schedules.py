"""Schedule endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from plantos_backend.repositories.plants import plant_repository
from plantos_backend.schemas.schedules import ScheduleDay
from plantos_backend.services import scheduler

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/merged", response_model=list[ScheduleDay])
def merged_schedule(horizon_days: int = 7) -> list[ScheduleDay]:
    tasks = scheduler.forecast_tasks(plant_repository.list(), horizon_days=horizon_days)
    grouped = scheduler.merge_tasks(tasks)
    return [
        ScheduleDay(date=date, tasks=sorted(tasks, key=lambda task: task.next_due_at))
        for date, tasks in sorted(grouped.items())
    ]
