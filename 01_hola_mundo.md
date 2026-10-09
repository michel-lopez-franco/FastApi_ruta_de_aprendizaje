# 01 — Hola mundo con FastAPI

**Código:** [`01_hola_mundo.py`](01_hola_mundo.py)

## ¿De qué trata?

Es la aplicación FastAPI más pequeña posible: crea la app, define dos rutas `GET` y devuelve JSON. Sirve para comprobar que el entorno funciona y para conocer la documentación automática que FastAPI genera sin escribir nada extra.

## ¿Qué aprenderás?

- Qué es la instancia `app = FastAPI()` y para qué sirven `title`, `description` y `version`.
- Cómo un **decorador** (`@app.get("/")`) asocia una función con un método HTTP y una ruta.
- Que un `dict` de Python se convierte automáticamente en una respuesta **JSON**.
- Cómo leer un valor de la URL con un **parámetro de ruta** (`/saludo/{name}`).
- Cómo levantar el servidor de desarrollo con recarga automática.
- Cómo usar **Swagger UI** (`/docs`) y **ReDoc** (`/redoc`) para explorar y probar la API.

## Conceptos clave

| Concepto | Qué es |
|---|---|
| **ASGI** | Estándar que conecta servidores web asíncronos con apps Python. |
| **Uvicorn** | El servidor ASGI que ejecuta la app (lo usa `fastapi dev` por debajo). |
| **Path operation** | La combinación *ruta + método HTTP* (p. ej. `GET /`). |
| **OpenAPI** | Especificación que FastAPI genera en `/openapi.json`; de ahí salen `/docs` y `/redoc`. |

## Ejecutar

```bash
uv run fastapi dev 01_hola_mundo.py
```

Visita:

- <http://127.0.0.1:8000> → `{"message": "Hola mundo desde FastAPI"}`
- <http://127.0.0.1:8000/saludo/Ana> → `{"message": "Hola, Ana"}`
- <http://127.0.0.1:8000/docs> → prueba los endpoints con **Try it out**

## Ejercicios

1. Agrega una ruta `GET /acerca` que devuelva el nombre del curso y tu nombre.
2. Cambia el `title` de la app y observa cómo cambia `/docs`.
3. Abre `/openapi.json` y localiza la ruta `/saludo/{name}`.
