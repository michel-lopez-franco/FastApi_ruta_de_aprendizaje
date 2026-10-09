"""Ejemplo 05 — Validación con Path, Query, Field y validadores custom.

Ejecutar:
    uv run fastapi dev 05_validacion.py

Probar valores inválidos para ver los errores 422:
    GET  /tasks/0                 (task_id debe ser >= 1)
    GET  /tasks?limit=500         (limit máximo 100)
    GET  /tasks?search=a          (search mínimo 3 caracteres)
    POST /tasks {"title": "  ", "estimated_hours": -1}
"""

from datetime import date
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="API de Tareas — validación")


class TaskCreate(BaseModel):
    # Field agrega restricciones y metadatos a los campos del modelo
    title: str = Field(min_length=3, max_length=100, examples=["Entregar práctica"])
    description: str | None = Field(default=None, max_length=500)
    estimated_hours: float = Field(default=1, gt=0, le=40)
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list, max_length=5)

    # Validador personalizado: lógica que no se puede expresar con Field
    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El título no puede estar vacío")
        return value.capitalize()

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("La fecha de entrega no puede estar en el pasado")
        return value


tasks: list[dict] = []


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate) -> dict:
    new_task = {"id": len(tasks) + 1, **task.model_dump()}
    tasks.append(new_task)
    return new_task


# Annotated[tipo, Query(...)] agrega restricciones a los query params
@app.get("/tasks")
def list_tasks(
    search: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de resultados")] = 10,
) -> list[dict]:
    result = tasks
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result[skip : skip + limit]


# Path(...) hace lo mismo para los parámetros de ruta
@app.get("/tasks/{task_id}")
def get_task(
    task_id: Annotated[int, Path(ge=1, description="ID de la tarea")],
) -> dict | None:
    return next((t for t in tasks if t["id"] == task_id), None)
