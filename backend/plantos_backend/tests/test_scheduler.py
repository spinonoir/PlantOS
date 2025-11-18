
from plantos_backend.models import CareSignal, Plant
from plantos_backend.services import scheduler


def test_forecast_tasks_filters_by_horizon():
    plant = Plant(name="Fern", watering_interval_days=1)
    tasks = scheduler.forecast_tasks([plant], horizon_days=1)
    assert tasks, "should create watering task"
    assert tasks[0].plant_id == plant.id


def test_merge_tasks_groups_by_date():
    plant = Plant(name="Monstera", watering_interval_days=1)
    care_task = scheduler.forecast_tasks([plant])[0]
    grouped = scheduler.merge_tasks([care_task])
    assert len(grouped) == 1
    key, value = next(iter(grouped.items()))
    assert key == care_task.next_due_at.date().isoformat()
    assert value[0].signal == CareSignal.watering
