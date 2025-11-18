import pytest

from plantos_backend.storage.memory import memory_store


@pytest.fixture(autouse=True)
def reset_store():
    memory_store.plants.clear()
    memory_store.care_tasks.clear()
    memory_store.timeline.clear()
    memory_store.experiments.clear()
    memory_store.propagations.clear()
    memory_store.listings.clear()
    memory_store.orders.clear()
    yield
