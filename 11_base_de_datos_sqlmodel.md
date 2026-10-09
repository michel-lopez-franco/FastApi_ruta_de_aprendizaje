# 11 — Base de datos con SQLModel

**Código:** [`11_base_de_datos_sqlmodel.py`](11_base_de_datos_sqlmodel.py)

## ¿De qué trata?

Hasta ahora los datos vivían en memoria y se perdían al reiniciar. Aquí conectamos la API a una **base de datos SQLite** usando **SQLModel** (creado por el mismo autor de FastAPI) e implementamos un **CRUD completo y persistente**.

> **SQLite vs. SQLModel:** no son alternativas, trabajan juntas.
>
> - **SQLite** es la **base de datos**: un archivo local (`tareas.db`) en tu computadora. No necesita instalar ni levantar ningún servidor.
> - **SQLModel** es la **librería de Python** que habla con esa base. Traduce las clases (`Task`) a tablas y las operaciones (`session.add`, `select`) a SQL.
>
> La línea que elige la base de datos es `DATABASE_URL = "sqlite:///tareas.db"`. Si la cambias por una URL de PostgreSQL o MySQL, el resto del código no cambia.

## ¿Qué aprenderás?

- Qué es un **ORM**: trabajar con tablas como si fueran clases de Python.
- Definir una tabla con `SQLModel` y `table=True`, con `id` como llave primaria autoincremental.
- Reutilizar campos con herencia: `TaskBase` → `Task` (tabla), `TaskCreate`, `TaskUpdate` (modelos de entrada).
- Crear el **engine** (conexión) y una **sesión por request** con una dependencia que usa `yield`.
- Crear las tablas al iniciar la app con **`lifespan`**.
- Las operaciones CRUD con la sesión:

  | Operación | Código |
  |---|---|
  | Crear | `session.add(task)` → `session.commit()` → `session.refresh(task)` |
  | Leer uno | `session.get(Task, task_id)` |
  | Leer varios | `session.exec(select(Task).where(...).offset(...).limit(...))` |
  | Actualizar | `task.sqlmodel_update(datos)` → `add` → `commit` |
  | Eliminar | `session.delete(task)` → `session.commit()` |

- Filtrar y paginar con `select().where().offset().limit()`.

## Dependencia con `yield`

```python
def get_session():
    with Session(engine) as session:
        yield session      # ← el endpoint se ejecuta aquí
    # al salir del with, la sesión se cierra automáticamente
```

El código antes del `yield` se ejecuta antes del endpoint, y el de después, al terminar el request. Es el patrón ideal para abrir y cerrar recursos.

## Ejecutar

```bash
uv run fastapi dev 11_base_de_datos_sqlmodel.py
```

1. Crea algunas tareas con `POST /tasks`.
2. **Detén y vuelve a iniciar** el servidor: las tareas siguen ahí.
3. Se generó el archivo `tareas.db`. Puedes abrirlo con la extensión *SQLite Viewer* de VS Code o con `sqlite3 tareas.db "SELECT * FROM task;"`.

## Siguiente paso: SQLite → PostgreSQL

Solo cambia la URL de conexión (idealmente desde variables de entorno):

```python
DATABASE_URL = "postgresql+psycopg://usuario:password@localhost:5432/tareas"
```

Para cambios de esquema en producción se usan **migraciones** con Alembic en lugar de `create_all`.

## Ejercicios

1. Agrega un campo `created_at: datetime` con valor por defecto a la hora actual.
2. Agrega un query param `search` que filtre por título usando `Task.title.contains(search)`.
3. Crea una tabla `User` y relaciona cada tarea con un usuario (`owner_id: int = Field(foreign_key="user.id")`).
