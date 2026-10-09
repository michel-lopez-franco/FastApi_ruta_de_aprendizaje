"""Ejemplo 11 — Base de datos con SQLModel: CRUD completo.

Ejecutar:
    uv run fastapi dev 11_base_de_datos_sqlmodel.py

Se crea el archivo tareas.db (SQLite) en la carpeta desde donde se ejecuta.
A diferencia de los ejemplos anteriores, los datos persisten al reiniciar.
"""

from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select


# --- Modelos -----------------------------------------------------------------
# SQLModel = Pydantic + SQLAlchemy: la misma clase valida datos y define tablas.
class TaskBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    done: bool = False


class Task(TaskBase, table=True):  # table=True -> es una tabla en la BD
    id: int | None = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    done: bool | None = None


# --- Conexión y sesión --------------------------------------------------------
DATABASE_URL = "sqlite:///tareas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Dependencia con yield: abre una sesión por request y la cierra al terminar
def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# lifespan: código que corre al iniciar (y al apagar) la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # crea las tablas si no existen
    yield


app = FastAPI(title="API de Tareas — SQLModel", lifespan=lifespan)


# --- CRUD ----------------------------------------------------------------------
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, session: SessionDep) -> Task:
    task = Task.model_validate(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)  # recarga el objeto para obtener el id generado
    return task


@app.get("/tasks")
def list_tasks(
    session: SessionDep,
    done: bool | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Task]:
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    return list(session.exec(statement.offset(skip).limit(limit)).all())


def get_task_or_404(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep) -> Task:
    return get_task_or_404(task_id, session)


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate, session: SessionDep) -> Task:
    task = get_task_or_404(task_id, session)
    task.sqlmodel_update(task_in.model_dump(exclude_unset=True))
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep) -> None:
    task = get_task_or_404(task_id, session)
    session.delete(task)
    session.commit()
