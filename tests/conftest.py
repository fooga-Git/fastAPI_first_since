import pytest
import asyncio
import subprocess
import os

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import engine, Base

PROJECT_PATH = os.getcwd()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Очищает БД и создаёт админа ОДИН РАЗ перед всеми тестами"""
    async def _clean():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_clean())
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_PATH

    subprocess.run([
        "poetry", "run", "python",
        "app/scripts/create_super_admin.py",
        "admin", "admin123"
    ], env=env, capture_output=True, text=True)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_token(client):
    client.post("/auth/register", data={
        "login": "testuser",
        "password": "123",
        "full_name": "Test User",
        "email": "test@example.com"
    })
    resp = client.post("/auth/login", data={
        "login": "testuser",
        "password": "123"
    })
    return resp.json()["access_token"]


@pytest.fixture
def admin_token(client):
    resp = client.post("/auth/login", data={
        "login": "admin",
        "password": "admin123"
    })
    return resp.json()["access_token"]
