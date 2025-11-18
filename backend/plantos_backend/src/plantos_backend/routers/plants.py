"""Plant and schedule APIs."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from plantos_backend.repositories.plants import plant_repository
from plantos_backend.schemas.plants import (
    CareTaskResponse,
    DueTask,
    PlantCreate,
    PlantResponse,
    PlantUpdate,
    TimelineEventCreate,
    TimelineEventResponse,
)
from plantos_backend.services import reminders

router = APIRouter(prefix="/plants", tags=["plants"])


@router.get("", response_model=list[PlantResponse])
def list_plants() -> list[PlantResponse]:
    return plant_repository.list()


@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_plant(payload: PlantCreate) -> PlantResponse:
    return plant_repository.create(payload)


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: str) -> PlantResponse:
    plant = plant_repository.get(plant_id)
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant


@router.patch("/{plant_id}", response_model=PlantResponse)
def update_plant(plant_id: str, payload: PlantUpdate) -> PlantResponse:
    plant = plant_repository.update(plant_id, payload)
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: str) -> None:
    existed = plant_repository.delete(plant_id)
    if not existed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")


@router.get("/{plant_id}/tasks", response_model=list[CareTaskResponse])
def list_tasks(plant_id: str) -> list[CareTaskResponse]:
    if not plant_repository.get(plant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant_repository.list_tasks(plant_id)


@router.get("/tasks/due", response_model=list[DueTask])
def due_tasks(minutes: int = 120) -> list[DueTask]:
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


@router.post(
    "/{plant_id}/timeline",
    response_model=TimelineEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_timeline_event(plant_id: str, payload: TimelineEventCreate) -> TimelineEventResponse:
    if not plant_repository.get(plant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant_repository.add_timeline_event(plant_id, payload)


@router.get("/{plant_id}/timeline", response_model=list[TimelineEventResponse])
def list_timeline(plant_id: str) -> list[TimelineEventResponse]:
    if not plant_repository.get(plant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant_repository.list_timeline(plant_id)
