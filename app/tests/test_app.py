from app import app, DB_FILE

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

def test_create_todo():
    client = app.test_client()
    response = client.post("/todos", json={"task": "New Task"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"] == "New Task"
    assert data["done"] is False

def test_update_todo():
    client = app.test_client()
    response = client.post("/todos", json={"task": "Temp Task"})
    todo_id = response.get_json()["id"]

    response = client.put(f"/todos/{todo_id}", json={"done": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["done"] is True

def test_delete_todo():
    client = app.test_client()
    response = client.post("/todos", json={"task": "Delete Me"})
    todo_id = response.get_json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Deleted"
