"""Ejemplo 01 — Hola mundo con FastAPI.

Ejecutar:
    uv run fastapi dev 01_hola_mundo.py

Abrir:
    http://127.0.0.1:8000        -> respuesta JSON
    http://127.0.0.1:8000/docs   -> Swagger UI (documentación interactiva)
    http://127.0.0.1:8000/redoc  -> ReDoc
"""

from fastapi import FastAPI

# La instancia de FastAPI es la aplicación: aquí se registran todas las rutas.
app = FastAPI(
    title="API de Tareas",
    description="Primer ejemplo del curso de FastAPI",
    version="0.1.0",
)


# El decorador asocia la función con el método GET en la ruta "/".
@app.get("/")
def read_root() -> dict[str, str]:
    # Lo que se retorna se convierte automáticamente a JSON.
    return {"message": "Hola mundo desde FastAPI"}


@app.get("/saludo/{name}")
def greet(name: str) -> dict[str, str]:
    return {"message": f"Hola, {name}"}
