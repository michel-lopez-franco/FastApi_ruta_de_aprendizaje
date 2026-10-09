# Ruta de aprendizaje: FastAPI desde cero

Índice de los temas necesarios para aprender FastAPI y poder trabajar con él en proyectos reales. Está ordenado de lo más básico a lo más avanzado: cada bloque se apoya en el anterior.

> Dominio de ejemplo que usaremos en todo el curso: **una API de tareas** (`/tasks`).

## Ejemplos prácticos de esta carpeta

Cada ejemplo tiene un `.py` ejecutable y un `.md` que explica de qué trata y qué aprenderás. Ejecútalos desde esta carpeta:
 

```bash
uv run fastapi dev 01_hola_mundo.py   # luego abre http://127.0.0.1:8000/docs
uv run pytest 12_testing.py -v        # el ejemplo 12 se ejecuta con pytest
```

| # | Ejemplo | Explicación | Tema |
|---|---|---|---|
| 01 | [`01_hola_mundo.py`](01_hola_mundo.py) | [`01_hola_mundo.md`](01_hola_mundo.md) | Primera app, Swagger UI y ReDoc |
| 02 | [`02_rutas_y_metodos.py`](02_rutas_y_metodos.py) | [`02_rutas_y_metodos.md`](02_rutas_y_metodos.md) | GET/POST/PUT/DELETE y path params |
| 03 | [`03_query_params.py`](03_query_params.py) | [`03_query_params.md`](03_query_params.md) | Filtros, paginación y Enums |
| 04 | [`04_modelos_pydantic.py`](04_modelos_pydantic.py) | [`04_modelos_pydantic.md`](04_modelos_pydantic.md) | Request body y modelos de respuesta |
| 05 | [`05_validacion.py`](05_validacion.py) | [`05_validacion.md`](05_validacion.md) | `Field`, `Query`, `Path` y validadores |
| 06 | [`06_dependencias.py`](06_dependencias.py) | [`06_dependencias.md`](06_dependencias.md) | Inyección de dependencias con `Depends` |
| 07 | [`07_errores_y_middlewares.py`](07_errores_y_middlewares.py) | [`07_errores_y_middlewares.md`](07_errores_y_middlewares.md) | `HTTPException`, handlers, middlewares y CORS |
| 08 | [`08_routers.py`](08_routers.py) | [`08_routers.md`](08_routers.md) | `APIRouter` y estructura del proyecto |
| 09 | [`09_configuracion.py`](09_configuracion.py) | [`09_configuracion.md`](09_configuracion.md) | Variables de entorno con `pydantic-settings` |
| 10 | [`10_autenticacion_jwt.py`](10_autenticacion_jwt.py) | [`10_autenticacion_jwt.md`](10_autenticacion_jwt.md) | Login, hash de contraseñas y JWT |
| 11 | [`11_base_de_datos_sqlmodel.py`](11_base_de_datos_sqlmodel.py) | [`11_base_de_datos_sqlmodel.md`](11_base_de_datos_sqlmodel.md) | CRUD persistente con SQLModel + SQLite |
| 12 | [`12_testing.py`](12_testing.py) | [`12_testing.md`](12_testing.md) | Pruebas con pytest y `TestClient` |

---

## Parte 0 — Prerrequisitos

Antes de tocar FastAPI conviene dominar estas bases.

### 0.1 Python moderno
- Variables, tipos básicos, listas, diccionarios, funciones
- Módulos, paquetes e imports
- Clases y objetos (lo básico de POO)
- **Type hints**: `int`, `str`, `list[str]`, `dict[str, int]`, `X | None`, `Annotated`
- Decoradores (qué hace `@app.get(...)`)
- Manejo de excepciones (`try` / `except` / `raise`)

### 0.2 Programación asíncrona (lo esencial)
- Qué es concurrencia vs. paralelismo
- `async def` y `await`
- Cuándo usar `def` y cuándo `async def` en FastAPI

### 0.3 Fundamentos de la web
- Modelo cliente–servidor
- Protocolo **HTTP**: request, response, headers, body
- Métodos HTTP: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- Códigos de estado: `2xx`, `3xx`, `4xx`, `5xx`
- Formato **JSON**
- Qué es una **API REST** y buenas prácticas de diseño de rutas

### 0.4 Herramientas de trabajo
- Terminal básica (navegar, ejecutar comandos)
- Entornos virtuales y gestión de dependencias con **uv**
- Git y GitHub
- Clientes HTTP para probar APIs: Swagger UI, `curl`, Postman/Bruno/HTTPie

---

## Parte 1 — Fundamentos de FastAPI

### 1. Introducción (`01_introduccion`)
- Qué es FastAPI y por qué usarlo (rendimiento, tipado, documentación automática)
- Piezas que lo forman: **Starlette** (web) + **Pydantic** (datos)
- Qué es ASGI y qué hace **Uvicorn**
- Instalación y primer endpoint "Hola mundo"
- Documentación automática: **Swagger UI** (`/docs`) y **ReDoc** (`/redoc`)

### 2. Rutas y parámetros (`02_rutas_y_parametros`)
- Path operations: `@app.get`, `@app.post`, `@app.put`, `@app.delete`
- Parámetros de ruta (path params): `/tasks/{task_id}`
- Parámetros de consulta (query params): `/tasks?done=true&limit=10`
- Parámetros opcionales y valores por defecto
- Orden de las rutas y conflictos
- Enums para valores predefinidos

### 3. Modelos con Pydantic (`03_modelos_pydantic`)
- `BaseModel` y campos tipados
- Request body: recibir JSON
- Response model: controlar lo que se devuelve (`response_model` / tipo de retorno)
- Modelos de entrada vs. salida (`TaskCreate`, `TaskRead`, `TaskUpdate`)
- Validación automática y errores `422`
- Modelos anidados y listas

---

## Parte 2 — Construyendo APIs sólidas

### 4. Validación y dependencias (`04_validacion_dependencias`)
- `Query`, `Path`, `Body` con restricciones (`min_length`, `gt`, `le`, ...)
- `Annotated` para declarar parámetros
- `Field` y validadores personalizados (`field_validator`)
- Inyección de dependencias con `Depends`
- Dependencias reutilizables (paginación, parámetros comunes)

### 5. Middlewares y manejo de errores (`05_middlewares_manejo_errores`)
- `HTTPException` y códigos de estado correctos
- Exception handlers personalizados
- Qué es un middleware y cómo crear uno
- **CORS**: permitir que un frontend consuma la API
- Headers, cookies y objeto `Request` / `Response`

### 6. Organización del proyecto
- `APIRouter` para separar rutas por recurso
- Estructura de carpetas recomendada (`routers/`, `models/`, `services/`)
- Configuración con variables de entorno (`pydantic-settings`, `.env`)

---

## Parte 3 — Funcionalidades de producción

### 7. Autenticación y seguridad (`06_autenticacion`)
- Autenticación vs. autorización
- Hash de contraseñas (nunca guardarlas en texto plano)
- OAuth2 con *password flow*
- Tokens **JWT**: generar, firmar y verificar
- Proteger rutas con `Depends(get_current_user)`
- Roles y permisos básicos

### 8. Bases de datos (`07_bases_de_datos`)
- Repaso de SQL y bases relacionales
- ORM: **SQLModel** (o SQLAlchemy)
- Conexión, motor y sesiones (sesión como dependencia)
- CRUD completo: crear, leer, actualizar, eliminar
- Relaciones entre tablas (uno a muchos)
- Migraciones con **Alembic** (introducción)

### 9. Testing (`08_testing`)
- Por qué probar una API
- **pytest**: estructura de pruebas y fixtures
- `TestClient` para probar endpoints
- Sobrescribir dependencias en pruebas (`app.dependency_overrides`)
- Base de datos de prueba

### 10. Despliegue (`09_despliegue`)
- `fastapi dev` vs. `fastapi run`
- Uvicorn / Gunicorn en producción
- Variables de entorno y secretos
- **Docker**: `Dockerfile` para una app FastAPI
- Opciones de hosting (Render, Railway, Fly.io, VPS)

---

## Parte 4 — Temas avanzados (opcionales)

- Tareas en segundo plano (`BackgroundTasks`)
- Subida y descarga de archivos (`UploadFile`)
- WebSockets
- Streaming y Server-Sent Events (SSE)
- Eventos de ciclo de vida (`lifespan`)
- Servir archivos estáticos y un frontend
- Caché y rate limiting
- Logging y monitoreo
- Bases de datos asíncronas

---

## Proyecto integrador sugerido

Al terminar, el alumno debería poder construir una **API de tareas completa** con:

- [ ] CRUD de tareas con validación Pydantic
- [ ] Usuarios con registro, login y JWT
- [ ] Cada usuario solo ve y edita sus propias tareas
- [ ] Persistencia en base de datos (SQLite → PostgreSQL)
- [ ] Pruebas automáticas con pytest
- [ ] Contenedor Docker listo para desplegar

---

## Recursos

- Documentación oficial: <https://fastapi.tiangolo.com/es/>
- Pydantic: <https://docs.pydantic.dev/>
- SQLModel: <https://sqlmodel.tiangolo.com/>
- uv: <https://docs.astral.sh/uv/>
