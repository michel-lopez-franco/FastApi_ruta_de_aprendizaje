# 02 — Rutas y métodos HTTP

**Código:** [`02_rutas_y_metodos.py`](02_rutas_y_metodos.py)

## ¿De qué trata?

Construimos un **CRUD básico de tareas** guardado en memoria (un diccionario). Cada operación usa el método HTTP que le corresponde según las convenciones REST.

## ¿Qué aprenderás?

- Los cuatro métodos principales y su significado:

  | Método | Ruta | Acción |
  |---|---|---|
  | `GET` | `/tasks` | Listar todas las tareas |
  | `GET` | `/tasks/{task_id}` | Obtener una tarea |
  | `POST` | `/tasks` | Crear una tarea |
  | `PUT` | `/tasks/{task_id}` | Modificar una tarea |
  | `DELETE` | `/tasks/{task_id}` | Eliminar una tarea |

- Que el **tipo** de un parámetro de ruta (`task_id: int`) hace que FastAPI convierta el texto de la URL a entero y responda `422` si no es válido (prueba `/tasks/abc`).
- Cómo cambiar el código de estado de respuesta con `status_code=201` al crear.
- Por qué importa el **orden de declaración** de las rutas cuando hay rutas fijas y rutas con parámetros.
- Que los datos en memoria se pierden al reiniciar el servidor (lo resolveremos en el ejemplo 11).

## Ejecutar

```bash
uv run fastapi dev 02_rutas_y_metodos.py
```

En `/docs`:

1. `GET /tasks` → ve las dos tareas iniciales.
2. `POST /tasks` con `title=Practicar` → nueva tarea con `id: 3`.
3. `PUT /tasks/3` con `done=true`.
4. `DELETE /tasks/1` y vuelve a listar.

## Limitaciones intencionales

Este ejemplo **no** valida bien los errores (devuelve `{"error": ...}` con código `200`) y recibe los datos como parámetros sueltos. Lo corregiremos en los ejemplos 04 (modelos) y 07 (`HTTPException`).

## Ejercicios

1. Agrega `GET /tasks/{task_id}/title` que devuelva solo el título.
2. Agrega `DELETE /tasks` que borre todas las tareas completadas.
3. Prueba `/tasks/1.5` y `/tasks/-1`: ¿qué responde cada una y por qué?
