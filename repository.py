from sqlalchemy import select

from database import TaskTable, new_session
from schemas import STask, Staskadd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: Staskadd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskTable(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskTable)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [
                STask.model_validate(task_model, from_attributes=True)
                for task_model in task_models
            ]
            return task_schemas
