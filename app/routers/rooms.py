from datetime import date

from sqlalchemy.exc import IntegrityError
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from app.core.database import new_session
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.models import Booking, Room, Slot, User
from app.repositories.room_repository import get_room_or_404
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.core.constants import DAY_SLOTS, NIGHT_SLOTS
from app.schemas.slot import SlotResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=List[RoomResponse], summary="Получение комнат")
async def get_rooms(
    _: User = Depends(get_current_user),
):
    async with new_session() as session:
        return (await session.execute(select(Room))).scalars().all()


@router.post("/", response_model=RoomResponse, summary="Создание комнат")
async def create_room(
    room_data: Annotated[RoomCreate, Depends()],
    _: Annotated[User, Depends(require_admin)],
):
    async with new_session() as session:
        try:
            room = Room(**room_data.model_dump())
            session.add(room)
            await session.flush()

            for slot in DAY_SLOTS:
                session.add(Slot(room_id=room.id, **slot))

            if room_data.room_type == "podcast":
                for slot in NIGHT_SLOTS:
                    session.add(Slot(room_id=room.id, **slot))

            await session.commit()
            await session.refresh(room)
            return room
        except IntegrityError:
            await session.rollback()
            raise HTTPException(409, "Комната с этим название уже существует.")


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(
    room_id: int,
    _: Annotated[User, Depends(require_admin)],
):
    room = await get_room_or_404(room_id)
    async with new_session() as session:
        await session.delete(room)
        await session.commit()
        return {"ok": True}


@router.patch("/{room_id}", summary="Редактирование комнат")
async def update_room(
    room_id: int,
    room_data: Annotated[RoomUpdate, Depends()],
    _: Annotated[User, Depends(require_admin)]
):
    room = await get_room_or_404(room_id)
    update_data = room_data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(room, key, value)

    async with new_session() as session:
        session.add(room)
        await session.commit()
        await session.refresh(room)
        return room


@router.get(
    "/{room_id}/slots",
    response_model=list[SlotResponse],
    summary="Получение слотов для комнат",
)
async def get_slots_by_room(
    room_id: int,
    date: date | None = Query(
        None, description="Если указать дату в формате YYYY-MM-DD,"
        " вернутся только свободные слоты на эту дату"),
    _: User = Depends(get_current_user),
):
    async with new_session() as session:
        query = select(Slot).where(Slot.room_id == room_id)
        slots = (await session.execute(query)).scalars().all()

        if date:
            booked = await session.execute(
                select(Booking.slot_id).where(
                    Booking.room_id == room_id,
                    Booking.date == date,
                    Booking.status == "active"
                )
            )
            booked_ids = {b[0] for b in booked}
            slots = [s for s in slots if s.id not in booked_ids]

        return [SlotResponse.model_validate(s) for s in slots]
