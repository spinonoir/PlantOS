from datetime import datetime, timezone
from plantos_backend.models.plants import Plant, CareTask, TimelineEvent, Reminder, LightLevel
from plantos_backend.models.common import CollectionNames, CareSignal

def test_plant_model_collection():
    assert Plant.collection_name == CollectionNames.plants
    
    plant = Plant(name="Monstera", species="Monstera Deliciosa", light_level=LightLevel.high)
    assert plant.id.startswith("plant_")
    assert plant.collection_name == CollectionNames.plants
    
    data = plant.model_dump()
    assert data["name"] == "Monstera"
    assert "id" in data
    assert "created_at" in data

def test_care_task_collection():
    assert CareTask.collection_name == CollectionNames.tasks
    
    task = CareTask(
        plant_id="plant_123",
        signal=CareSignal.watering,
        cadence_days=7,
        next_due_at=datetime.now(timezone.utc)
    )
    assert task.id.startswith("task_")
    assert task.priority == "medium"

def test_timeline_event_collection():
    assert TimelineEvent.collection_name == CollectionNames.events
    
    event = TimelineEvent(
        plant_id="plant_123",
        event_type="watered",
        note="Watered thoroughly"
    )
    assert event.id.startswith("event_")

def test_reminder_collection():
    assert Reminder.collection_name == CollectionNames.reminders
    
    reminder = Reminder(
        task_id="task_123",
        send_at=datetime.now(timezone.utc)
    )
    assert reminder.id.startswith("reminder_")
