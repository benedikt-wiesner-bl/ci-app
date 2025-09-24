import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_get_todos():
    client = app.test_client()
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "task" in data[0]

def test_create_todo():
    client = app.test_client()
    response = client.post("/todos", json={"task": "New Task"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"] == "New Task"
    assert data["done"] is False

def test_update_todo():
    client = app.test_client()
    response = client.put("/todos/1", json={"done": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["done"] is True

def test_delete_todo():
    client = app.test_client()
    response = client.delete("/todos/2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Deleted"
