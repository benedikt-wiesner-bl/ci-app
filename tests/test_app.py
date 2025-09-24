import sqlite3
import pytest
from app import app, DB_FILE

@pytest.fixture(autouse=True)
def setup_db():
    """Vor jedem Test DB leeren + 2 Dummy-Todos anlegen."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM todos")
    c.execute("INSERT INTO todos (task, done) VALUES ('Task 1', 0)")
    c.execute("INSERT INTO todos (task, done) VALUES ('Task 2', 1)")
    conn.commit()
    conn.close()
    yield


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
