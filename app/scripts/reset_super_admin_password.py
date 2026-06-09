import asyncio
import getpass

from sqlalchemy import select

from app.core.database import new_session
from app.models import User
from app.core.security import get_password_hash


async def reset_password():
    print("=== Сброс пароля супер админа ===\n")

    login = input("Введите логин супер админа: ").strip()
    if not login:
        print("Логин обязателен")
        return

    new_password = getpass.getpass("Новый пароль: ")
    if not new_password:
        print("Пароль обязателен")
        return

    confirm = getpass.getpass("Подтвердите пароль: ")
    if new_password != confirm:
        print("Пароли не совпадают")
        return

    async with new_session() as session:
        result = await session.execute(
            select(User).where(User.login == login, User.role == "admin")
        )
        user = result.scalar_one_or_none()

        if not user:
            print("Супер админ не найден")
            return

        user.password_hash = get_password_hash(new_password)
        await session.commit()
        print(f"ароль для {login} успешно изменён")


if __name__ == "__main__":
    asyncio.run(reset_password())
