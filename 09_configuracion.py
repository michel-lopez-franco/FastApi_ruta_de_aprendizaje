"""Ejemplo 09 — Configuración con variables de entorno (pydantic-settings).

Ejecutar:
    uv run fastapi dev 09_configuracion.py

Cambiar la configuración sin tocar el código:
    APP_NAME="Mis Tareas" MAX_TASKS_PER_USER=3 uv run fastapi dev 09_configuracion.py

O crear un archivo .env en esta carpeta:
    APP_NAME="Mis Tareas"
    DEBUG=true
    SECRET_KEY=cambia-esto
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Cada campo se lee de la variable de entorno con el mismo nombre
    # (sin importar mayúsculas). Si no existe, se usa el valor por defecto.
    app_name: str = "API de Tareas"
    debug: bool = False
    max_tasks_per_user: int = 50
    database_url: str = "sqlite:///tareas.db"
    # Sin valor por defecto -> obligatorio en producción. Aquí ponemos uno
    # de desarrollo para que el ejemplo arranque sin configurar nada.
    secret_key: str = "solo-para-desarrollo"

    model_config = SettingsConfigDict(env_file=".env")


# lru_cache: el archivo .env y el entorno se leen una sola vez
@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]

app = FastAPI(title=get_settings().app_name)


@app.get("/info")
def app_info(settings: SettingsDep) -> dict:
    # Nunca expongas secretos (secret_key, contraseñas) en una respuesta
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "max_tasks_per_user": settings.max_tasks_per_user,
    }
