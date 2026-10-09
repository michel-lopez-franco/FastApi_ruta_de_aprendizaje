# 06 — Inyección de dependencias con `Depends`

**Código:** [`06_dependencias.py`](06_dependencias.py)

## ¿De qué trata?

Las **dependencias** son funciones que FastAPI ejecuta *antes* de tu endpoint y cuyo resultado te entrega como parámetro. Son la herramienta principal de FastAPI para **reutilizar lógica**: paginación, acceso a base de datos, usuario autenticado, configuración…

## ¿Qué aprenderás?

- Crear una dependencia (una función normal) y usarla con `Depends`.
- Que las dependencias **también leen del request**: query params, headers, body…
- Crear **alias de tipo** reutilizables:

  ```python
  PaginationDep = Annotated[Pagination, Depends(get_pagination)]

  @app.get("/tasks")
  def list_tasks(pagination: PaginationDep): ...
  ```

- Reutilizar la misma dependencia en varios endpoints (`/tasks` y `/tasks-pending`).
- Leer **headers** con `Header()` (`X-Request-Source` → `x_request_source`).
- La idea de un **repositorio** inyectado, que en el ejemplo 11 se convierte en una sesión de base de datos y en el ejemplo 12 se reemplaza en las pruebas.

## ¿Por qué no simplemente llamar a la función?

| Llamar la función tú mismo | Usar `Depends` |
|---|---|
| Tienes que pasarle los datos del request a mano | FastAPI le inyecta los datos del request |
| No aparece en `/docs` | Sus parámetros se documentan solos |
| Difícil de reemplazar en pruebas | Se sustituye con `app.dependency_overrides` |

## Ejecutar

```bash
uv run fastapi dev 06_dependencias.py
```

- `/tasks?skip=1&limit=1`
- `/tasks?limit=100` → `422` (la validación vive en la dependencia)
- `/tasks/1` desde `/docs` llenando el header `x-request-source`

## Ejercicios

1. Crea una dependencia `get_order` con un query param `order` (`asc`/`desc`) y úsala en `/tasks`.
2. Crea una dependencia que lance `HTTPException(status_code=401)` si el header `X-Api-Key` no es `"curso-fastapi"`, y aplícala a un endpoint (adelanto del ejemplo 07).
3. Aplica esa misma dependencia a **toda la app** con `FastAPI(dependencies=[Depends(...)])`.
