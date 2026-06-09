from typing import Annotated
from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Информация о текущем пользователе",
)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
