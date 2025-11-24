"""Schedule and task feed APIs."""
from __future__ import annotations

from fastapi import APIRouter

from plantos_backend.repositories.plants import plant_repository
from plantos_backend.schemas.plants import DueTask
from plantos_backend.services import reminders

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/due", response_model=list[DueTask])
def due_tasks(minutes: int = 120) -> list[DueTask]:
    """Get tasks due within the next N minutes."""
    tasks = reminders.due_within(plant_repository.list_tasks(), minutes=minutes)
    return [
        DueTask(
            task_id=task.id,
            plant_id=task.plant_id,
            signal=task.signal.value,
            next_due_at=task.next_due_at,
        )
        for task in tasks
    ]
