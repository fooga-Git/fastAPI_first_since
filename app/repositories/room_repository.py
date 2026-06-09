from fastapi import HTTPException

from app.core.database import new_session
from app.models import Room


async def get_room_or_404(room_id: int) -> Room:
    async with new_session() as session:
        room = await session.get(Room, room_id)
        if not room:
            raise HTTPException(404, "Комната не найдена.")
        return room
