from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models import User


async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Не остаточно прав.")
    return current_user
