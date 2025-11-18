"""Marketplace endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from plantos_backend.models.marketplace import ListingStatus
from plantos_backend.schemas.marketplace import (
    ListingCreate,
    ListingResponse,
    ListingUpdate,
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from plantos_backend.services import marketplace as marketplace_service

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


@router.post("/listings", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(payload: ListingCreate) -> ListingResponse:
    provenance = [f"mother:{payload.batch_id}"]
    return marketplace_service.create_listing(payload, provenance=provenance)


@router.get("/listings", response_model=list[ListingResponse])
def list_listings(status: ListingStatus | None = None) -> list[ListingResponse]:
    return marketplace_service.list_listings(status)


@router.patch("/listings/{listing_id}", response_model=ListingResponse)
def update_listing(listing_id: str, payload: ListingUpdate) -> ListingResponse:
    try:
        return marketplace_service.update_listing(listing_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate) -> OrderResponse:
    try:
        return marketplace_service.create_order(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, payload: OrderUpdate) -> OrderResponse:
    try:
        return marketplace_service.update_order(order_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
