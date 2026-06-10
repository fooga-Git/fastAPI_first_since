from fastapi import Form
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.repositories.user_repository import get_user_or_error
from app.schemas.token import Token
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
async def register(
    login: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
):
    async with new_session() as session:
        existing = await session.execute(
            select(User).where((User.login == login) | (User.email == email))
        )
        if existing.scalar_one_or_none():
            raise HTTPException(400, "Данное значение уже используется")

        hashed = get_password_hash(password)
        user = User(
            login=login,
            password_hash=hashed,
            full_name=full_name,
            email=email,
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
async def login(
    login: str = Form(...),
    password: str = Form(...),
):
    async with new_session() as session:
        stmt = select(User).where(User.login == login)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(401, "Неверный логин или пароль.")

        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token({"user_id": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


@router.post("/refresh", response_model=Token, summary="Обновление токена")
async def refresh_token(refresh_token: str = Form(...)):
    payload = decode_token(refresh_token)
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
