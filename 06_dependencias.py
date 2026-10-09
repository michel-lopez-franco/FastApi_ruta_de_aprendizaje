"""Ejemplo 06 — Inyección de dependencias con Depends.

Ejecutar:
    uv run fastapi dev 06_dependencias.py

Probar:
    /tasks?skip=0&limit=2
    /tasks/1   con y sin el header  X-Request-Source: docs
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, Query
from pydantic import BaseModel

app = FastAPI(title="API de Tareas — dependencias")

tasks = [
    {"id": 1, "title": "Instalar uv", "done": True},
    {"id": 2, "title": "Aprender FastAPI", "done": False},
    {"id": 3, "title": "Repasar HTTP", "done": False},
]


# 1) Dependencia simple: una función que FastAPI ejecuta antes del endpoint.
#    Sus parámetros también se leen del request (aquí, query params).
class Pagination(BaseModel):
    skip: int
    limit: int


def get_pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> Pagination:
    return Pagination(skip=skip, limit=limit)


# Alias reutilizable: se usa como tipo en cualquier endpoint
PaginationDep = Annotated[Pagination, Depends(get_pagination)]


# 2) Una dependencia puede usar otra dependencia (dependencias en cadena)
def get_task_repository() -> list[dict]:
    # En el ejemplo 11 esto será una sesión de base de datos
    return tasks


TaskRepoDep = Annotated[list[dict], Depends(get_task_repository)]


# 3) Dependencia que lee un header
def get_request_source(
    x_request_source: Annotated[str | None, Header()] = None,
) -> str:
    return x_request_source or "desconocido"


SourceDep = Annotated[str, Depends(get_request_source)]


@app.get("/tasks")
def list_tasks(pagination: PaginationDep, repo: TaskRepoDep) -> dict:
    items = repo[pagination.skip : pagination.skip + pagination.limit]
    return {"pagination": pagination, "items": items}


@app.get("/tasks/{task_id}")
def get_task(task_id: int, repo: TaskRepoDep, source: SourceDep) -> dict:
    task = next((t for t in repo if t["id"] == task_id), None)
    return {"source": source, "task": task}


# La misma dependencia de paginación, reutilizada en otro endpoint
@app.get("/tasks-pending")
def list_pending(pagination: PaginationDep, repo: TaskRepoDep) -> list[dict]:
    pending = [t for t in repo if not t["done"]]
    return pending[pagination.skip : pagination.skip + pagination.limit]
