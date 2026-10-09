# 04 — Modelos Pydantic: request body y response model

**Código:** [`04_modelos_pydantic.py`](04_modelos_pydantic.py)

## ¿De qué trata?

Reescribimos el CRUD de tareas usando **modelos Pydantic** para describir qué datos entran (body JSON) y qué datos salen (respuesta). FastAPI usa esos modelos para validar, convertir, filtrar y documentar automáticamente.

## ¿Qué aprenderás?

- Definir modelos con `BaseModel` y campos tipados.
- Que un parámetro cuyo tipo es un `BaseModel` se lee del **body** de la petición como JSON.
- Separar modelos por propósito, un patrón muy usado en proyectos reales:

  | Modelo | Para qué |
  |---|---|
  | `TaskCreate` | Lo que el cliente envía al **crear** (sin `id`) |
  | `TaskUpdate` | Lo que el cliente envía al **actualizar** (todo opcional) |
  | `TaskRead` | Lo que la API **devuelve** (incluye `id` y `done`) |

- Usar el **tipo de retorno** (`-> TaskRead`) como modelo de respuesta: valida y filtra la salida.
- La **validación automática**: si falta un campo o el tipo es incorrecto, FastAPI responde `422` con el detalle del error sin que escribas código.
- Modelos **anidados** (`TaskList` contiene una `list[TaskRead]`).
- Actualizaciones parciales con `PATCH` usando `model_dump(exclude_unset=True)` y `model_copy(update=...)`.

## Ejecutar

```bash
uv run fastapi dev 04_modelos_pydantic.py
```

En `/docs`, `POST /tasks` con:

```json
{"title": "Estudiar Pydantic", "description": "Capítulo 3"}
```

Luego prueba bodies inválidos: `{}` o `{"title": ["no", "es", "texto"]}` y revisa la respuesta `422`.

Observa también la sección **Schemas** al final de `/docs`: ahí aparecen tus modelos.

## Ejercicios

1. Agrega un campo `priority: int = 1` a la tarea y propágalo a los tres modelos donde corresponda.
2. Crea un `PUT /tasks/{task_id}` que reemplace la tarea completa con `TaskCreate`.
3. Agrega a `TaskRead` un campo que NO debería ver el cliente (p. ej. `internal_note`) y crea un modelo público que lo oculte.
