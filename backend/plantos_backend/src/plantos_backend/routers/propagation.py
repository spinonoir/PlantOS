"""Propagation routes."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from plantos_backend.schemas.propagation import (
    PropagationCreate,
    PropagationResponse,
    PropagationUpdate,
)
from plantos_backend.services import propagation as propagation_service

router = APIRouter(prefix="/propagation", tags=["propagation"])


@router.post("", response_model=PropagationResponse, status_code=status.HTTP_201_CREATED)
def create_batch(payload: PropagationCreate) -> PropagationResponse:
    return propagation_service.create_batch(payload)


@router.get("", response_model=list[PropagationResponse])
def list_batches(mother_plant_id: str | None = None) -> list[PropagationResponse]:
    return propagation_service.list_batches(mother_plant_id)


@router.patch("/{batch_id}", response_model=PropagationResponse)
def update_batch(batch_id: str, payload: PropagationUpdate) -> PropagationResponse:
    try:
        return propagation_service.update_batch(batch_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{batch_id}/ready", response_model=PropagationResponse)
def mark_ready(batch_id: str) -> PropagationResponse:
    try:
        return propagation_service.mark_ready(batch_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
