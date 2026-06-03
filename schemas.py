from pydantic import BaseModel


class Staskadd(BaseModel):
    name: str
    description: str | None = None


class STask(Staskadd):
    id: int


class STaskId(BaseModel):
    ok: bool = True
    task_id: int