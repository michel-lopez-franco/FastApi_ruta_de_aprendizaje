"""Ejemplo 02 — Rutas, métodos HTTP y parámetros de ruta.

Ejecutar:
    uv run fastapi dev 02_rutas_y_metodos.py

Los datos viven en memoria (un diccionario): al reiniciar el servidor se pierden.
"""

from fastapi import FastAPI

app = FastAPI(title="API de Tareas — rutas y métodos")

# "Base de datos" en memoria: id -> tarea
tasks: dict[int, dict] = {
    1: {"id": 1, "title": "Instalar uv", "done": True},
    2: {"id": 2, "title": "Leer la documentación de FastAPI", "done": False},
}


# GET: leer la colección completa
@app.get("/tasks")
def list_tasks() -> list[dict]:
    return list(tasks.values())


# GET con parámetro de ruta: el tipo `int` convierte y valida el valor
@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> dict:
    return tasks.get(task_id, {"error": "Tarea no encontrada"})


# Las rutas fijas deben declararse ANTES que una ruta con parámetro que pueda
# coincidir. Aquí no hay conflicto porque /tasks/{task_id} exige un entero,
# pero si fuera `str`, "/tasks/pending" sería capturada por la ruta anterior.
@app.get("/stats/pending")
def count_pending() -> dict[str, int]:
    return {"pending": sum(1 for t in tasks.values() if not t["done"])}


# POST: crear un recurso. Por ahora recibimos el título como parámetro simple;
# en el ejemplo 04 lo haremos con un modelo Pydantic en el body.
@app.post("/tasks", status_code=201)
def create_task(title: str) -> dict:
    new_id = max(tasks, default=0) + 1
    tasks[new_id] = {"id": new_id, "title": title, "done": False}
    return tasks[new_id]


# PUT: actualizar un recurso existente
@app.put("/tasks/{task_id}")
def complete_task(task_id: int, done: bool) -> dict:
    if task_id not in tasks:
        return {"error": "Tarea no encontrada"}
    tasks[task_id]["done"] = done
    return tasks[task_id]


# DELETE: eliminar un recurso
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    removed = tasks.pop(task_id, None)
    return {"deleted": removed is not None}
