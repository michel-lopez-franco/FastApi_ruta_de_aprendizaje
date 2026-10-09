# 10 — Autenticación con OAuth2 y JWT

**Código:** [`10_autenticacion_jwt.py`](10_autenticacion_jwt.py)

## ¿De qué trata?

Implementamos un **login** que devuelve un **token JWT** y protegemos rutas para que solo un usuario autenticado pueda usarlas. Además, cada usuario ve **únicamente sus propias tareas**. Es el flujo estándar que usan la mayoría de las APIs que consume un frontend o una app móvil.

## ¿Qué aprenderás?

- La diferencia entre **autenticación** (¿quién eres?) y **autorización** (¿qué puedes hacer?).
- Guardar contraseñas como **hash** (Argon2 con `pwdlib`) y verificarlas, nunca en texto plano.
- El flujo **OAuth2 Password**: el cliente envía usuario y contraseña a `/token` y recibe un token.
- Qué es un **JWT**: un token firmado con datos (`sub` = usuario, `exp` = expiración).
- Crear y verificar tokens con `PyJWT`.
- Usar `OAuth2PasswordBearer` para leer el header `Authorization: Bearer <token>`.
- Proteger rutas con una dependencia: `current_user: CurrentUserDep`.
- Responder `401` con el header `WWW-Authenticate` cuando el token falta, es inválido o expiró.
- Usar el botón **Authorize** de `/docs`.

## El flujo completo

```
1. POST /token  (username + password)
        │
        ▼
   ¿contraseña correcta? ── no ──► 401
        │ sí
        ▼
   {"access_token": "eyJhbGciOi...", "token_type": "bearer"}

2. GET /tasks   Header: Authorization: Bearer eyJhbGciOi...
        │
        ▼
   get_current_user ── firma inválida / expirado ──► 401
        │ válido
        ▼
   endpoint recibe current_user y filtra sus tareas
```

## Anatomía de un JWT

Un JWT tiene tres partes separadas por puntos: `header.payload.firma`. El payload **no está cifrado**, solo codificado en base64: cualquiera puede leerlo en <https://jwt.io>, pero **nadie puede modificarlo** sin la `SECRET_KEY`, porque la firma deja de coincidir. Por eso nunca se guardan datos sensibles en el payload.

## Ejecutar

```bash
uv run fastapi dev 10_autenticacion_jwt.py
```

1. `GET /tasks` sin autorizar → `401`.
2. Botón **Authorize** → usuario `ana`, contraseña `secreto123`.
3. `GET /users/me` y `GET /tasks` → ahora funcionan; solo aparece la tarea de Ana.
4. Copia el token y pégalo en <https://jwt.io> para ver su contenido.

## Ejercicios

1. Agrega un segundo usuario `luis` y verifica que cada uno ve solo sus tareas.
2. Crea `POST /tasks` protegido que asigne automáticamente `owner = current_user.username`.
3. Agrega un campo `role` (`"admin"` / `"user"`) y una dependencia `require_admin` que responda `403` si el usuario no es admin.
4. Mueve `SECRET_KEY` a la configuración con variables de entorno del ejemplo 09.
