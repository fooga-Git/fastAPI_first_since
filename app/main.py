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
from app.scripts.create_super_admin import create_super_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_super_admin("admin", "admin123")
    print("✅ Супер админ создан (или уже существует)")
    yield

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
