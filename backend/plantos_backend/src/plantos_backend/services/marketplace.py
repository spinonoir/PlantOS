"""Marketplace orchestration."""
from __future__ import annotations

from typing import List

from plantos_backend.models import Listing, ListingStatus, Order, OrderStatus
from plantos_backend.schemas.marketplace import (
    ListingCreate,
    ListingUpdate,
    OrderCreate,
    OrderUpdate,
)
from plantos_backend.storage.memory import memory_store


def create_listing(payload: ListingCreate, provenance: list[str] | None = None) -> Listing:
    listing = Listing(**payload.model_dump(), provenance=provenance or [])
    memory_store.listings[listing.id] = listing
    return listing


def list_listings(status: ListingStatus | None = None) -> List[Listing]:
    listings = list(memory_store.listings.values())
    if status:
        listings = [listing for listing in listings if listing.status == status]
    return listings


def update_listing(listing_id: str, payload: ListingUpdate) -> Listing:
    listing = memory_store.listings.get(listing_id)
    if not listing:
        raise ValueError("Listing not found")
    listing = listing.model_copy(update=payload.model_dump(exclude_unset=True))
    memory_store.listings[listing_id] = listing
    return listing


def create_order(payload: OrderCreate) -> Order:
    listing = memory_store.listings.get(payload.listing_id)
    if not listing:
        raise ValueError("Listing not found")
    listing = listing.model_copy(update={"status": ListingStatus.reserved})
    memory_store.listings[listing.id] = listing
    order = Order(
        listing_id=payload.listing_id,
        buyer_name=payload.buyer_name,
        total=listing.price,
        currency=listing.currency,
    )
    memory_store.orders[order.id] = order
    return order


def update_order(order_id: str, payload: OrderUpdate) -> Order:
    order = memory_store.orders.get(order_id)
    if not order:
        raise ValueError("Order not found")
    order = order.model_copy(update=payload.model_dump())
    memory_store.orders[order_id] = order
    if payload.status == OrderStatus.fulfilled:
        listing = memory_store.listings.get(order.listing_id)
        if listing:
            listing = listing.model_copy(update={"status": ListingStatus.sold})
            memory_store.listings[listing.id] = listing
    return order
