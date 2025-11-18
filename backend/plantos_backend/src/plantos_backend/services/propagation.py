"""Propagation services."""
from __future__ import annotations

from typing import List, Optional

from plantos_backend.models import PropagationBatch, PropagationStage
from plantos_backend.schemas.propagation import PropagationCreate, PropagationUpdate
from plantos_backend.storage.memory import memory_store


def create_batch(payload: PropagationCreate) -> PropagationBatch:
    batch = PropagationBatch(**payload.model_dump())
    memory_store.propagations[batch.id] = batch
    return batch


def list_batches(mother_plant_id: Optional[str] = None) -> List[PropagationBatch]:
    batches = list(memory_store.propagations.values())
    if mother_plant_id:
        batches = [batch for batch in batches if batch.mother_plant_id == mother_plant_id]
    return batches


def update_batch(batch_id: str, payload: PropagationUpdate) -> PropagationBatch:
    batch = memory_store.propagations.get(batch_id)
    if not batch:
        raise ValueError("Batch not found")
    update_data = payload.model_dump(exclude_unset=True)
    batch = batch.model_copy(update=update_data)
    memory_store.propagations[batch_id] = batch
    return batch


def mark_ready(batch_id: str) -> PropagationBatch:
    batch = memory_store.propagations.get(batch_id)
    if not batch:
        raise ValueError("Batch not found")
    batch = batch.model_copy(update={"stage": PropagationStage.sale_ready})
    memory_store.propagations[batch_id] = batch
    return batch
