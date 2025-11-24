"""Reminder scheduling helpers."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, List

from plantos_backend.models import CareTask


def due_within(tasks: Iterable[CareTask], minutes: int = 120) -> List[CareTask]:
    now = datetime.now(timezone.utc)
    window = now + timedelta(minutes=minutes)
    return [task for task in tasks if task.next_due_at <= window]


def enqueue_reminders(tasks: List[CareTask]) -> List[str]:
    """
    Stub for enqueuing push notifications.
    In a real system, this would push to a queue or call Firebase Cloud Messaging.
    Returns a list of reminder IDs generated.
    """
    reminder_ids = []
    for task in tasks:
        # In a real implementation, we would create a Reminder document here
        # and send the notification.
        # For now, we just simulate it.
        print(f"Enqueuing reminder for task {task.id} (due {task.next_due_at})")
        reminder_ids.append(f"rem_{task.id}")
    return reminder_ids

