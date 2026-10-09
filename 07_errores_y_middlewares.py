"""Ejemplo 07 — HTTPException, exception handlers, middlewares y CORS.

Ejecutar:
    uv run fastapi dev 07_errores_y_middlewares.py

Probar:
    GET    /tasks/99        -> 404 con HTTPException
    DELETE /tasks/1         -> 409 con excepción propia + handler
    Revisar los headers de cualquier respuesta: X-Process-Time
"""

import time

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="API de Tareas — errores y middlewares")

tasks = {
    1: {"id": 1, "title": "Instalar uv", "done": True, "locked": True},
    2: {"id": 2, "title": "Aprender FastAPI", "done": False, "locked": False},
}


# --- CORS -----------------------------------------------------------------
# Permite que un frontend en otro origen (p. ej. Vite en el puerto 5173)
# consuma esta API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Middleware propio -------------------------------------------------------
# Se ejecuta en CADA request: antes y después del endpoint.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)  # aquí se ejecuta el endpoint
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response


# --- Excepción propia + handler ------------------------------------------
class TaskLockedError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id


@app.exception_handler(TaskLockedError)
async def task_locked_handler(request: Request, exc: TaskLockedError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "task_locked",
            "detail": f"La tarea {exc.task_id} está bloqueada y no se puede modificar",
        },
    )


# --- Endpoints -------------------------------------------------------------
def find_task(task_id: int) -> dict:
    task = tasks.get(task_id)
    if task is None:
        # HTTPException corta la ejecución y responde con el código indicado
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe la tarea {task_id}",
        )
    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> dict:
    return find_task(task_id)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    task = find_task(task_id)
    if task["locked"]:
        raise TaskLockedError(task_id)
    del tasks[task_id]
