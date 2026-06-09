from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models import User
from app.core.security import decode_token
from app.repositories.user_repository import get_user_or_error


security = HTTPBearer(
    description="JWT токен в формате: Bearer <ваш_токен>"
)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(401, "Invalid token")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(401, "Invalid token payload")

    return await get_user_or_error(int(user_id), status_code=401)
