from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_tables
from app.routers import (
    admin,
    auth,
    bookings,
    users,
    rooms,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Сервер запущен")
    yield
    print("Сервер остановлен")

app = FastAPI(
    title="Booking Service API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(admin.router)
app.include_router(bookings.router)
