"""Ejemplo 08 — Organizar la API con APIRouter.

Ejecutar:
    uv run fastapi dev 08_routers.py

En un proyecto real cada router va en su propio archivo
(p. ej. routers/tasks.py, routers/users.py) y main.py solo los incluye.
Aquí están en un solo archivo para que el ejemplo sea autocontenido.
Observa en /docs cómo los endpoints aparecen agrupados por tags.
"""

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    owner_id: int


class User(BaseModel):
    id: int
    name: str


tasks = [
    Task(id=1, title="Aprender routers", owner_id=1),
    Task(id=2, title="Separar el proyecto en archivos", owner_id=2),
]
users = [User(id=1, name="Ana"), User(id=2, name="Luis")]


# ===== routers/tasks.py =====
# prefix y tags se declaran en el router, no en include_router()
tasks_router = APIRouter(prefix="/tasks", tags=["tareas"])


@tasks_router.get("/")
def list_tasks() -> list[Task]:
    return tasks


@tasks_router.get("/{task_id}")
def get_task(task_id: int) -> Task | None:
    return next((t for t in tasks if t.id == task_id), None)


# ===== routers/users.py =====
users_router = APIRouter(prefix="/users", tags=["usuarios"])


@users_router.get("/")
def list_users() -> list[User]:
    return users


@users_router.get("/{user_id}/tasks")
def list_user_tasks(user_id: int) -> list[Task]:
    return [t for t in tasks if t.owner_id == user_id]


# ===== main.py =====
app = FastAPI(title="API de Tareas — routers")

# Un router puede incluir a otros: así se versiona la API (/api/v1/...)
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(tasks_router)
api_v1.include_router(users_router)

app.include_router(api_v1)


@app.get("/", tags=["salud"])
def health() -> dict[str, str]:
    return {"status": "ok"}
