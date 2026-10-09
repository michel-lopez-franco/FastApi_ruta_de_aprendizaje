# 09 — Configuración con variables de entorno

**Código:** [`09_configuracion.py`](09_configuracion.py)

## ¿De qué trata?

El código no debe contener contraseñas, URLs de bases de datos ni claves secretas: esos valores cambian entre tu computadora, el servidor de pruebas y producción. Este ejemplo usa **`pydantic-settings`** para leer la configuración de **variables de entorno** y de un archivo **`.env`**, con validación de tipos incluida.

## ¿Qué aprenderás?

- Definir la configuración como una clase `BaseSettings` con tipos y valores por defecto.
- Cómo cada campo se lee de la variable de entorno con el mismo nombre (`APP_NAME` → `app_name`).
- Cargar valores desde un archivo `.env` con `SettingsConfigDict(env_file=".env")`.
- Que los valores se **validan**: `MAX_TASKS_PER_USER=abc` falla al arrancar.
- Leer la configuración **una sola vez** con `@lru_cache`.
- Inyectar la configuración en los endpoints como dependencia (`SettingsDep`).
- No exponer secretos en las respuestas y **no subir `.env` a Git**.

## Orden de prioridad

1. Variables de entorno del sistema
2. Archivo `.env`
3. Valores por defecto de la clase

## Ejecutar

```bash
uv run fastapi dev 09_configuracion.py
```

`GET /info` muestra los valores por defecto. Ahora cámbialos sin tocar el código:

```bash
APP_NAME="Mis Tareas" DEBUG=true uv run fastapi dev 09_configuracion.py
```

O crea un archivo `.env` junto al script:

```env
APP_NAME="Mis Tareas"
MAX_TASKS_PER_USER=5
SECRET_KEY=una-clave-larga-y-aleatoria
```

> Agrega `.env` a tu `.gitignore` y sube en su lugar un `.env.example` sin valores reales.

## Ejercicios

1. Quita el valor por defecto de `secret_key` y observa el error al arrancar sin definirla.
2. Agrega un campo `allowed_origins: list[str]` y úsalo para configurar CORS (ejemplo 07).
3. Usa `settings.debug` para mostrar u ocultar `/docs` (`FastAPI(docs_url=None)`).
