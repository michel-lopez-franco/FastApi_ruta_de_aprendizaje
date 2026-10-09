# 12 — Pruebas automáticas con pytest

**Código:** [`12_testing.py`](12_testing.py)

## ¿De qué trata?

Probar una API a mano en `/docs` no escala: cada cambio puede romper algo que ya funcionaba. Aquí escribimos **pruebas automáticas** con `pytest` y el `TestClient` de FastAPI, que hace peticiones a la app **sin levantar un servidor**.

## ¿Qué aprenderás?

- Usar `TestClient(app)` para hacer peticiones `GET`, `POST`, etc. en pruebas.
- Escribir pruebas con `assert` sobre el **código de estado** y el **JSON** de respuesta.
- Probar el camino feliz **y** los errores (`422`, `404`).
- Crear **fixtures** de pytest para preparar el estado antes de cada prueba.
- **Reemplazar dependencias** con `app.dependency_overrides` para que cada prueba use su propio almacenamiento (en un proyecto real, una base de datos de prueba).
- Por qué las pruebas deben ser **independientes** entre sí.

## Anatomía de una prueba

```python
def test_create_task(client):
    # 1. Arrange / Act: ejecutar la acción
    response = client.post("/tasks", json={"title": "Escribir pruebas"})
    # 2. Assert: verificar el resultado
    assert response.status_code == 201
    assert response.json()["title"] == "Escribir pruebas"
```

## Ejecutar

```bash
uv run pytest 12_testing.py -v
```

Resultado esperado:

```
12_testing.py::test_create_task PASSED
12_testing.py::test_create_task_invalid_title PASSED
12_testing.py::test_get_task PASSED
12_testing.py::test_get_missing_task PASSED
```

> En un proyecto real las pruebas van en una carpeta `tests/` con archivos `test_*.py`, y basta con ejecutar `uv run pytest`.

## Ejercicios

1. Comenta la línea de `dependency_overrides` y ejecuta las pruebas: ¿cuáles fallan y por qué?
2. Agrega un endpoint `DELETE /tasks/{task_id}` y escribe una prueba para el caso exitoso y otra para el `404`.
3. Escribe pruebas para el ejemplo 10: login correcto, login incorrecto y acceso a `/users/me` con y sin token.
