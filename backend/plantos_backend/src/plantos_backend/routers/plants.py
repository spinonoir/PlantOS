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
from plantos_backend.services import reminders, scheduler

router = APIRouter(prefix="/plants", tags=["plants"])


@router.get("", response_model=list[PlantResponse])
def list_plants() -> list[PlantResponse]:
    return plant_repository.list()


@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_plant(payload: PlantCreate) -> PlantResponse:
    plant = plant_repository.create(payload)
    # Generate initial tasks
    tasks = scheduler.generate_initial_tasks(plant)
    for task in tasks:
        plant_repository.add_task(task)
    return plant


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




@router.post("/tasks/{task_id}/complete", response_model=CareTaskResponse)
def complete_task(task_id: str) -> CareTaskResponse:
    task = plant_repository.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    plant = plant_repository.get(task.plant_id)
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")

    updated_task, event = scheduler.complete_task(task, plant)
    
    plant_repository.update_task(updated_task)
    plant_repository.add_timeline_event(plant.id, TimelineEventCreate(
        event_type=event.event_type,
        note=event.note,
        photo_url=event.photo_url
    ))
    
    return updated_task


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
