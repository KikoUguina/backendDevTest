from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_get_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "This is a test task"
    })
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert "id" in task

    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    assert any(t["id"] == task["id"] for t in get_response.json())

def test_update_task():
    response = client.post("/tasks", json={
        "title": "Old Title",
        "description": "Old Description"
    })
    task = response.json()

    update_response = client.put(f"/tasks/{task['id']}", json={
        "title": "New Title",
        "description": "New Description"
    })
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "New Title"

def test_delete_task():
    response = client.post("/tasks", json={
        "title": "Delete me",
        "description": "This task will be deleted"
    })
    task_id = response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    get_response = client.get("/tasks")
    assert not any(t["id"] == task_id for t in get_response.json())
