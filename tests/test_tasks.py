
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import getDb
from app.main import app
from app.models import Base

# Create a separate, temporary in-memory SQLite database for tests.
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[getDb] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


# ---------- Root endpoint ----------

def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task Management API is running"
    }


# ---------- Create task ----------

def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker",
            "description": "Containerize my FastAPI project",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Containerize my FastAPI project"
    assert data["status"] is False
    assert isinstance(data["id"], int)
    assert "created_at" in data


def test_create_task_missing_title(client):
    response = client.post(
        "/tasks",
        json={"description": "A task without a title"},
    )

    assert response.status_code == 422


def test_create_task_missing_description(client):
    response = client.post(
        "/tasks",
        json={"title": "Missing description"},
    )

    assert response.status_code == 422


def test_create_task_empty_body(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


# ---------- Retrieve tasks ----------

def test_get_all_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Task One", "description": "First task"},
    )
    client.post(
        "/tasks",
        json={"title": "Task Two", "description": "Second task"},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client):
    created = client.post(
        "/tasks",
        json={"title": "Find me", "description": "Retrieve this task"},
    )
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Find me"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ---------- Update task ----------

def test_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Old title", "description": "Old description"},
    )
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["description"] == "Updated description"
    assert response.json()["status"] is True


def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/99999",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": True,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_missing_required_field(client):
    created = client.post(
        "/tasks",
        json={"title": "Original", "description": "Original description"},
    )
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated title"},
    )

    assert response.status_code == 422


# ---------- Complete task ----------

def test_complete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Finish testing", "description": "Complete all tests"},
    )
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    assert response.json()["status"] is True


def test_complete_nonexistent_task(client):
    response = client.patch("/tasks/99999/complete")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ---------- Delete task ----------

def test_delete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Delete me", "description": "Test deletion"},
    )
    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
