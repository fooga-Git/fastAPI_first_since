from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.core.database import new_session
from app.core.permissions import require_admin
from app.models import User
from app.repositories.user_repository import get_user_or_error
from app.schemas.user import SetRoleRequest

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/set-role", summary="Назначение роли")
async def set_user_role(
    data: Annotated[SetRoleRequest, Depends()],
    _: Annotated[User, Depends(require_admin)]
):
    if data.user_id == 1:
        raise HTTPException(403, "Отказ в доступе.")

    user = await get_user_or_error(data.user_id, status_code=404)
    user.role = data.role

    async with new_session() as session:
        session.add(user)
        await session.commit()

    return {"ok": True}


@router.delete("/users/{user_id}", summary="Удаление сотрудника")
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(require_admin)]
):
    if user_id == 1:
        raise HTTPException(403, "Нельзя удалять Супер-администратора.")
    if current_user.id == user_id:
        raise HTTPException(400, "Нельзя удалять самого себяю.")

    user = await get_user_or_error(user_id, status_code=404)

    async with new_session() as session:
        await session.delete(user)
        await session.commit()

    return {"ok": True}
