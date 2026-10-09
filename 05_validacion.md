# 05 — Validación de datos

**Código:** [`05_validacion.py`](05_validacion.py)

## ¿De qué trata?

Más allá de los tipos, una API necesita **reglas de negocio**: títulos con longitud mínima, horas positivas, fechas que no estén en el pasado, límites de paginación… Este ejemplo muestra todas las formas de declarar esas reglas en FastAPI y Pydantic.

## ¿Qué aprenderás?

- **`Field`** para restricciones en modelos: `min_length`, `max_length`, `gt`, `ge`, `lt`, `le`, `default_factory`, `examples`.
- **`Query`** y **`Path`** para restricciones en parámetros de URL.
- El estilo recomendado **`Annotated[tipo, Query(...)]`**.
- **Validadores personalizados** con `@field_validator` para reglas que no caben en `Field`:
  - limpiar/transformar el valor (quitar espacios, capitalizar)
  - lanzar `ValueError` con un mensaje propio
- Tipos especiales que Pydantic valida solo: `date`, `list[str]`, `float`.
- Leer e interpretar el JSON de error `422` (`loc`, `msg`, `type`).

## Restricciones numéricas

| Restricción | Significado |
|---|---|
| `gt=0` | mayor que 0 |
| `ge=0` | mayor o igual que 0 |
| `lt=100` | menor que 100 |
| `le=100` | menor o igual que 100 |

## Ejecutar

```bash
uv run fastapi dev 05_validacion.py
```

Provoca errores a propósito:

- `GET /tasks/0`: `task_id` debe ser `>= 1`.
- `GET /tasks?limit=500`: máximo 100.
- `GET /tasks?search=a`: mínimo 3 caracteres.
- `POST /tasks` con `{"title": "   ", "estimated_hours": -1}`: dos errores a la vez.
- `POST /tasks` con `{"title": "Tarea", "due_date": "2020-01-01"}`: el mensaje del validador propio.

## Ejercicios

1. Agrega `@field_validator("tags")` que convierta todas las etiquetas a minúsculas y elimine duplicadas.
2. Restringe `title` para que no pueda contener la palabra `"prueba"`.
3. Agrega un query param `min_hours` que solo acepte valores entre 0 y 40.
