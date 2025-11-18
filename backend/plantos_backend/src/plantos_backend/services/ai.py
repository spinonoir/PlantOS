"""AI orchestration helpers."""
from __future__ import annotations

from plantos_backend.ai.graphs import (
    EXPERIMENT_GRAPH,
    HEALTH_CHECK_GRAPH,
    PLANT_ONBOARD_GRAPH,
)


def run_onboarding(photo_url: str | None, notes: str | None) -> dict:
    state = {"photo_url": photo_url, "notes": notes}
    return PLANT_ONBOARD_GRAPH.invoke(state)


def run_health_check(description: str) -> dict:
    return HEALTH_CHECK_GRAPH.invoke({"description": description})


def run_experiment_review(payload: dict) -> dict:
    return EXPERIMENT_GRAPH.invoke(payload)
