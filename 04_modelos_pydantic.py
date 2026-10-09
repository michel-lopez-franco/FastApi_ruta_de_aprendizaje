"""Ejemplo 04 — Modelos Pydantic: request body y response model.

Ejecutar:
    uv run fastapi dev 04_modelos_pydantic.py

Probar en /docs el POST /tasks enviando:
    {"title": "Estudiar Pydantic", "description": "Capítulo 3"}
Y luego enviar algo inválido, p. ej. {"title": 123} o {} para ver el error 422.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API de Tareas — modelos Pydantic")


# Modelo de ENTRADA para crear: solo lo que el cliente puede enviar
class TaskCreate(BaseModel):
    title: str
    description: str | None = None


# Modelo de ENTRADA para actualizar: todos los campos opcionales
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None


# Modelo de SALIDA: lo que la API devuelve al cliente
class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool = False


# Modelo anidado: una lista de tareas con metadatos
class TaskList(BaseModel):
    total: int
    items: list[TaskRead]


tasks: dict[int, TaskRead] = {}


# Un parámetro cuyo tipo es un BaseModel se lee del BODY (JSON).
# El tipo de retorno (-> TaskRead) valida, filtra y documenta la respuesta.
@app.post("/tasks", status_code=201)
def create_task(task_in: TaskCreate) -> TaskRead:
    new_id = len(tasks) + 1
    task = TaskRead(id=new_id, **task_in.model_dump())
    tasks[new_id] = task
    return task


@app.get("/tasks")
def list_tasks() -> TaskList:
    return TaskList(total=len(tasks), items=list(tasks.values()))


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> TaskRead | None:
    return tasks.get(task_id)


# PATCH: actualización parcial. exclude_unset=True ignora los campos
# que el cliente no envió, para no sobrescribirlos con None.
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate) -> TaskRead | None:
    task = tasks.get(task_id)
    if task is None:
        return None
    changes = task_in.model_dump(exclude_unset=True)
    updated = task.model_copy(update=changes)
    tasks[task_id] = updated
    return updated
