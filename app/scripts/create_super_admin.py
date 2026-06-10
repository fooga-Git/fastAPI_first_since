import asyncio
import sys

from sqlalchemy import select

from app.core.database import new_session
from app.models import User
from app.core.security import get_password_hash


async def create_super_admin(login: str = "admin", password: str = "admin123"):
    async with new_session() as session:
        result = await session.execute(
            select(User).where(User.login == login))
        if result.scalar_one_or_none():
            print("Админ уже существует")
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
        print(f"✅ Супер админ создан: {login}")


if __name__ == "__main__":
    login = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin123"
    asyncio.run(create_super_admin(login, password))
