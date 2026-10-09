# 07 — Manejo de errores y middlewares

**Código:** [`07_errores_y_middlewares.py`](07_errores_y_middlewares.py)

## ¿De qué trata?

Una API profesional responde con el **código de estado HTTP correcto** cuando algo sale mal y aplica lógica común a todas las peticiones. Este ejemplo muestra cómo lanzar errores, cómo personalizarlos, cómo interceptar cada request con un middleware y cómo habilitar CORS para un frontend.

## ¿Qué aprenderás?

- Lanzar **`HTTPException`** para cortar la ejecución y responder `404`, `400`, `401`, etc.
- Usar las constantes de `fastapi.status` (`status.HTTP_404_NOT_FOUND`) en vez de números sueltos.
- Crear una **excepción propia** (`TaskLockedError`) y convertirla en una respuesta JSON con **`@app.exception_handler`**. Así la lógica de negocio no depende de HTTP.
- Responder `204 No Content` en un `DELETE` exitoso.
- Escribir un **middleware** que se ejecuta antes y después de cada request (aquí mide el tiempo y agrega el header `X-Process-Time`).
- Configurar **CORS** con `CORSMiddleware` para que un frontend en otro origen (React, Vue, etc.) pueda llamar a la API desde el navegador.

## Flujo de un request con middleware

```
Cliente ──► Middleware (antes) ──► Endpoint ──► Middleware (después) ──► Cliente
                                      │
                                      └─ raise HTTPException / TaskLockedError
                                             └─► exception handler ──► JSON de error
```

## Códigos de estado más comunes

| Código | Cuándo usarlo |
|---|---|
| `200 OK` | Lectura o actualización correcta |
| `201 Created` | Recurso creado |
| `204 No Content` | Eliminado, sin cuerpo de respuesta |
| `400 Bad Request` | Petición incorrecta según la lógica de negocio |
| `401 Unauthorized` | Falta autenticación o es inválida |
| `403 Forbidden` | Autenticado, pero sin permiso |
| `404 Not Found` | El recurso no existe |
| `409 Conflict` | Conflicto con el estado actual del recurso |
| `422 Unprocessable Entity` | Error de validación (lo genera FastAPI) |

## Ejecutar

```bash
uv run fastapi dev 07_errores_y_middlewares.py
```

- `GET /tasks/99` → `404`
- `DELETE /tasks/1` → `409` (tarea bloqueada, handler propio)
- `DELETE /tasks/2` → `204`
- Revisa los **Response headers** en `/docs`: aparece `x-process-time`.

## Ejercicios

1. Crea una excepción `TaskAlreadyDoneError` con su handler que responda `400`.
2. Escribe un middleware que imprima en consola el método, la ruta y el código de respuesta de cada request.
3. Personaliza el error `422`: registra un handler para `RequestValidationError` que devuelva `{"error": "datos_invalidos", "detalles": [...]}`.
