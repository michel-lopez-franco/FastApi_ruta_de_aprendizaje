"""Ejemplo 03 — Parámetros de consulta (query params) y Enums.

Ejecutar:
    uv run fastapi dev 03_query_params.py

Probar:
    /tasks
    /tasks?done=false
    /tasks?priority=alta&limit=2
    /tasks?search=fastapi&skip=1
"""

from enum import Enum

from fastapi import FastAPI

app = FastAPI(title="API de Tareas — query params")


# Un Enum restringe los valores válidos y aparece como lista desplegable en /docs
class Priority(str, Enum):
    low = "baja"
    medium = "media"
    high = "alta"


tasks = [
    {"id": 1, "title": "Instalar uv", "done": True, "priority": "baja"},
    {"id": 2, "title": "Aprender FastAPI", "done": False, "priority": "alta"},
    {"id": 3, "title": "Repasar HTTP", "done": False, "priority": "media"},
    {"id": 4, "title": "Practicar FastAPI con Pydantic", "done": False, "priority": "alta"},
]


# Todo parámetro de la función que NO esté en la ruta es un query param.
# - Con valor por defecto -> opcional
# - Sin valor por defecto -> obligatorio
# - `X | None = None`    -> opcional y puede no enviarse
@app.get("/tasks")
def list_tasks(
    done: bool | None = None,
    priority: Priority | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[dict]:
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority.value]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result[skip : skip + limit]


# Path param + query param juntos
@app.get("/tasks/{task_id}")
def get_task(task_id: int, uppercase: bool = False) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            if uppercase:
                return {**task, "title": task["title"].upper()}
            return task
    return {"error": "Tarea no encontrada"}
