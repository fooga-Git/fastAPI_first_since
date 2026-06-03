from typing import Annotated

from fastapi import Depends, APIRouter

from repository import TaskRepository
from schemas import STask, STaskId, Staskadd


router = APIRouter(
    prefix='/tasks',
    tags=["Таски"],
)


@router.post('')
async def add_task(
        task: Annotated[Staskadd, Depends()],
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get('')
async def get_tastks() -> list[STask]:
    tasks = await TaskRepository.get_all()
    return tasks
