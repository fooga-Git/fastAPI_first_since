from sqlalchemy import select
from fastapi import HTTPException

from app.core.database import new_session
from app.models import User


async def get_user_or_error(user_id: int, status_code: int = 404) -> User:
    async with new_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code, "Сотрудник не найден.")
        return user
