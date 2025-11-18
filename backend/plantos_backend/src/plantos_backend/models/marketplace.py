"""Marketplace and order models."""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from plantos_backend.models.common import TimestampedModel


class ListingStatus(str, Enum):
    draft = "draft"
    published = "published"
    reserved = "reserved"
    sold = "sold"


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    fulfilled = "fulfilled"
    cancelled = "cancelled"


class Listing(TimestampedModel):
    batch_id: str
    title: str
    price: float
    currency: str = "USD"
    status: ListingStatus = ListingStatus.draft
    description: str
    provenance: list[str] = Field(default_factory=list)
    photo_url: Optional[str] = None


class Order(TimestampedModel):
    listing_id: str
    buyer_name: str
    total: float
    currency: str = "USD"
    status: OrderStatus = OrderStatus.pending
    stripe_payment_intent: Optional[str] = None
