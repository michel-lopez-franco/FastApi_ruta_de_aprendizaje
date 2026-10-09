"""Ejemplo 10 — Autenticación con OAuth2 (password flow) y JWT.

Ejecutar:
    uv run fastapi dev 10_autenticacion_jwt.py

Probar en /docs:
    1. Botón "Authorize" -> usuario: ana  contraseña: secreto123
    2. GET /users/me y GET /tasks ahora funcionan (envían el token)
    3. Sin autorizar, esas rutas responden 401
"""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

# En un proyecto real estos valores vienen de variables de entorno (ejemplo 09).
# Generar una clave segura con:  openssl rand -hex 32
SECRET_KEY = "clave-de-desarrollo-cambiala-en-produccion-1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()  # Argon2

# Usuarios "registrados". Se guarda el HASH, nunca la contraseña en texto plano.
fake_users_db = {
    "ana": {
        "username": "ana",
        "full_name": "Ana López",
        "hashed_password": password_hash.hash("secreto123"),
    },
}

tasks = [
    {"id": 1, "title": "Tarea de Ana", "owner": "ana"},
    {"id": 2, "title": "Tarea de Luis", "owner": "luis"},
]


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    full_name: str


app = FastAPI(title="API de Tareas — autenticación JWT")

# Indica a FastAPI (y a /docs) en qué ruta se obtiene el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str) -> dict | None:
    user = fake_users_db.get(username)
    if user is None or not password_hash.verify(password, user["hashed_password"]):
        return None
    return user


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Dependencia de seguridad: lee el header "Authorization: Bearer <token>",
# verifica la firma y la expiración, y devuelve el usuario.
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise credentials_error
    user = fake_users_db.get(payload.get("sub"))
    if user is None:
        raise credentials_error
    return User(**user)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user["username"]), token_type="bearer")


# Ruta protegida: solo funciona con un token válido
@app.get("/users/me")
def read_me(current_user: CurrentUserDep) -> User:
    return current_user


# Autorización: el usuario solo ve SUS tareas
@app.get("/tasks")
def list_my_tasks(current_user: CurrentUserDep) -> list[dict]:
    return [t for t in tasks if t["owner"] == current_user.username]


# Ruta pública: no requiere token
@app.get("/")
def public() -> dict[str, str]:
    return {"message": "Esta ruta es pública"}
