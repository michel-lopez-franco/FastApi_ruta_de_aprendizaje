# 03 — Parámetros de consulta (query params)

**Código:** [`03_query_params.py`](03_query_params.py)

## ¿De qué trata?

Un endpoint de listado de tareas que acepta **filtros, búsqueda y paginación** a través de la *query string* (`?clave=valor&...`), más un `Enum` para restringir los valores de prioridad.

## ¿Qué aprenderás?

- La regla de FastAPI: **todo parámetro de la función que no aparece en la ruta es un query param**.
- La diferencia entre parámetros:
  - **obligatorios**: sin valor por defecto (`q: str`)
  - **opcionales con valor por defecto**: `limit: int = 10`
  - **opcionales que pueden faltar**: `done: bool | None = None`
- Cómo FastAPI convierte tipos: `?done=false`, `?done=0` y `?done=no` se vuelven `False`.
- Cómo usar un **`Enum`** para aceptar solo ciertos valores (`baja`, `media`, `alta`) y mostrarlos como lista en `/docs`.
- El patrón de paginación `skip` / `limit`.
- Combinar **path params y query params** en un mismo endpoint.

## Path param vs. query param

| | Path param | Query param |
|---|---|---|
| Ejemplo | `/tasks/2` | `/tasks?done=false` |
| Uso típico | Identificar **un** recurso | Filtrar, ordenar, paginar |
| ¿Opcional? | No | Sí (si tiene valor por defecto) |

## Ejecutar

```bash
uv run fastapi dev 03_query_params.py
```

Prueba:

- `/tasks?done=false`
- `/tasks?priority=alta&limit=1`
- `/tasks?search=fastapi`
- `/tasks?priority=urgente` → `422`, el valor no está en el `Enum`
- `/tasks/2?uppercase=true`

## Ejercicios

1. Agrega un query param `order` que acepte `asc` o `desc` (usa un `Enum`) y ordene por `id`.
2. Haz que `search` sea **obligatorio** en un nuevo endpoint `/tasks/search`.
3. ¿Qué pasa si envías `?limit=abc`? Explica el error que devuelve FastAPI.
