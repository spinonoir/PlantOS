"""Reminder scheduling helpers."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, List

from plantos_backend.models import CareTask


def due_within(tasks: Iterable[CareTask], minutes: int = 120) -> List[CareTask]:
    now = datetime.now(timezone.utc)
    window = now + timedelta(minutes=minutes)
    return [task for task in tasks if task.next_due_at <= window]


def postpone(task: CareTask, minutes: int) -> CareTask:
    updated = task.model_copy(update={"next_due_at": task.next_due_at + timedelta(minutes=minutes)})
    return updated
