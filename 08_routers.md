# 08 — Organizar la API con `APIRouter`

**Código:** [`08_routers.py`](08_routers.py)

## ¿De qué trata?

Cuando una API crece, poner todas las rutas en un solo archivo se vuelve inmanejable. `APIRouter` permite **agrupar endpoints por recurso** (tareas, usuarios…) y luego unirlos en la app principal. El ejemplo simula en un solo archivo lo que en un proyecto real serían varios.

## ¿Qué aprenderás?

- Crear routers con `APIRouter(prefix=..., tags=[...])`.
- Declarar `prefix`, `tags` y dependencias compartidas **en el router**, no al incluirlo.
- Incluir routers en la app con `app.include_router(...)`.
- **Anidar routers** para versionar la API (`/api/v1/tasks`, `/api/v1/users`).
- Cómo los `tags` agrupan los endpoints en `/docs`.
- Una estructura de carpetas típica para proyectos FastAPI.

## Estructura recomendada en un proyecto real

```
app/
├── main.py            # crea la app e incluye los routers
├── config.py          # Settings (ejemplo 09)
├── database.py        # engine y get_session (ejemplo 11)
├── models/
│   ├── task.py
│   └── user.py
└── routers/
    ├── tasks.py       # tasks_router = APIRouter(prefix="/tasks", ...)
    └── users.py
```

Y en `main.py`:

```python
from app.routers import tasks, users

app = FastAPI()
app.include_router(tasks.router)
app.include_router(users.router)
```

## Ejecutar

```bash
uv run fastapi dev 08_routers.py
```

- `/api/v1/tasks/`
- `/api/v1/users/2/tasks`
- Abre `/docs` y observa los grupos **tareas**, **usuarios** y **salud**.

## Ejercicios

1. Separa este archivo en una carpeta real con `main.py`, `routers/tasks.py` y `routers/users.py`.
2. Agrega un router `/api/v2/tasks` que devuelva las tareas con un formato distinto.
3. Agrega una dependencia a `users_router` (con `dependencies=[Depends(...)]`) que se aplique a todas sus rutas.
