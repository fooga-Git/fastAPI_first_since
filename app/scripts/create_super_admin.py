import asyncio
import getpass

from sqlalchemy import select

from app.core.database import new_session
from app.models import User
from app.core.security import get_password_hash


async def create_super_admin():
    print("=== Создание супер админа ===\n")

    login = input("Логин: ").strip()
    if not login:
        print("Логин обязателен")
        return

    password = getpass.getpass("Пароль: ")
    if not password:
        print("Пароль обязателен")
        return

    async with new_session() as session:
        result = await session.execute(select(User).where(User.id == 1))
        if result.scalar_one_or_none():
            print("Супер админ уже существует")
            return

        admin = User(
            login=login,
            password_hash=get_password_hash(password),
            full_name="Super Admin",
            email="admin@example.com",
            role="admin"
        )
        session.add(admin)
        await session.commit()
        print(f"Супер админ создан: {login}")


if __name__ == "__main__":
    asyncio.run(create_super_admin())
