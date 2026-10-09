"""Ejemplo 12 — Pruebas automáticas con pytest y TestClient.

Ejecutar las pruebas:
    uv run pytest 12_testing.py -v

La app y sus pruebas están en el mismo archivo para que el ejemplo sea
autocontenido. En un proyecto real las pruebas van en tests/test_*.py.
"""

from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


# ============================ La aplicación ============================
class TaskCreate(BaseModel):
    title: str = Field(min_length=3)


class TaskRead(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskRepository:
    """Almacenamiento en memoria. Se inyecta como dependencia."""

    def __init__(self) -> None:
        self.tasks: dict[int, TaskRead] = {}

    def add(self, task_in: TaskCreate) -> TaskRead:
        task = TaskRead(id=len(self.tasks) + 1, title=task_in.title)
        self.tasks[task.id] = task
        return task


repository = TaskRepository()


def get_repository() -> TaskRepository:
    return repository


RepoDep = Annotated[TaskRepository, Depends(get_repository)]

app = FastAPI()


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, repo: RepoDep) -> TaskRead:
    return repo.add(task_in)


@app.get("/tasks/{task_id}")
def get_task(task_id: int, repo: RepoDep) -> TaskRead:
    task = repo.tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


# ============================== Las pruebas ==============================
# Fixture: prepara un cliente con un repositorio NUEVO en cada prueba,
# para que las pruebas no dependan unas de otras.
@pytest.fixture
def client():
    test_repo = TaskRepository()
    app.dependency_overrides[get_repository] = lambda: test_repo
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    response = client.post("/tasks", json={"title": "Escribir pruebas"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Escribir pruebas", "done": False}


def test_create_task_invalid_title(client: TestClient):
    response = client.post("/tasks", json={"title": "ab"})
    assert response.status_code == 422


def test_get_task(client: TestClient):
    client.post("/tasks", json={"title": "Primera tarea"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Primera tarea"


def test_get_missing_task(client: TestClient):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarea no encontrada"}
