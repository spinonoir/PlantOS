from fastapi.testclient import TestClient

from plantos_backend.app import app

client = TestClient(app)


def test_create_and_list_plants():
    payload = {"name": "ZZ Plant", "species": "Zamioculcas"}
    create_resp = client.post("/plants", json=payload)
    assert create_resp.status_code == 201
    plant_id = create_resp.json()["id"]

    list_resp = client.get("/plants")
    assert list_resp.status_code == 200
    assert any(item["id"] == plant_id for item in list_resp.json())


def test_due_tasks_endpoint():
    resp = client.get("/plants/tasks/due")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
