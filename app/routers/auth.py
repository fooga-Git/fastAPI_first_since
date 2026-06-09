from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.repositories.user_repository import get_user_or_error
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import RefreshRequest, Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.database import new_session
from app.models import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", summary="Регистрация")
async def register(data: Annotated[UserCreate, Depends()]):
    async with new_session() as session:
        existing = await session.execute(
            select(User).where((User.login == data.login)
                               | (User.email == data.email))
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, "Данное значение уже используется")

        hashed = get_password_hash(data.password)
        user = User(
            login=data.login,
            password_hash=hashed,
            full_name=data.full_name,
            email=data.email,
            role="employee"
        )
        session.add(user)
        await session.commit()
        return {"ok": True, "user_id": user.id}


@router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему",
)
async def login(user_data: Annotated[UserLogin, Depends()]):
    async with new_session() as session:
        stmt = select(User).where(User.login == user_data.login)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(
            user_data.password,
            user.password_hash,
        ):
            raise HTTPException(401, "Неверный логин или пароль.")

        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token({"user_id": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


@router.post("/refresh", response_model=Token, summary="Обновление токена")
async def refresh_token(data: Annotated[RefreshRequest, Depends()]):
    payload = decode_token(data.refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(401, "Invalid refresh token payload")

    user = await get_user_or_error(int(user_id), status_code=401)

    new_access_token = create_access_token({"user_id": user.id})
    new_refresh_token = create_refresh_token({"user_id": user.id})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
