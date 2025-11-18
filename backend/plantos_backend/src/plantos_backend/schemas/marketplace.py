"""Schemas for marketplace endpoints."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from plantos_backend.models.marketplace import Listing, ListingStatus, Order, OrderStatus


class ListingCreate(BaseModel):
    batch_id: str
    title: str
    price: float
    currency: str = "USD"
    description: str
    photo_url: Optional[str] = None


class ListingUpdate(BaseModel):
    status: ListingStatus | None = None
    price: float | None = None
    description: str | None = None


class ListingResponse(Listing):
    pass


class OrderCreate(BaseModel):
    listing_id: str
    buyer_name: str


class OrderUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(Order):
    pass
