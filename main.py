from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tabels, delete_tabels
from router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tabels()
    print("Base clear")
    await create_tabels()
    print("Base ready")
    yield
    print("Off")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
