from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import new_session
from app.core.dependencies import get_current_user
from app.models import User, Slot, Booking
from app.repositories.room_repository import get_room_or_404
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post(
    "/",
    response_model=BookingResponse,
    summary="Создание Брони",
)
async def create_booking(
    data: Annotated[BookingCreate, Depends()],
    current_user: Annotated[User, Depends(get_current_user)]
):
    await get_room_or_404(data.room_id)
    async with new_session() as session:
        slot = await session.execute(
            select(Slot).where(
                Slot.room_id == data.room_id,
                Slot.number == data.slot_number
            )
        )
        slot = slot.scalar_one_or_none()
        if not slot:
            raise HTTPException(
                404, f"Слот {data.slot_number} не доступен для этой комнаты.")

        existing = await session.execute(
            select(Booking).where(
                Booking.room_id == data.room_id,
                Booking.slot_id == slot.id,
                Booking.date == data.date,
                Booking.status == "active"
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(409, "Слот уже забронирован на эту дату.")

        booking = Booking(
            user_id=current_user.id,
            room_id=data.room_id,
            slot_id=slot.id,
            date=data.date,
            status="active"
        )
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking


@router.delete("/{booking_id}", summary="Удаление брони")
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user)
):
    async with new_session() as session:
        result = await session.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        booking = result.scalar_one_or_none()
        if not booking:
            raise HTTPException(404, "Бронь не найдена.")

        if booking.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(403, "Не достаточно прав.")

        await session.delete(booking)
        await session.commit()

        return {"ok": True}


@router.get(
    "/",
    response_model=list[BookingResponse],
    summary="Получение броней",
)
async def get_bookings(current_user: User = Depends(get_current_user)):
    async with new_session() as session:
        query = select(Booking).options(
            selectinload(Booking.slot),
            selectinload(Booking.room),
            selectinload(Booking.user),
        ).where(Booking.status == "active")

        if current_user.role != "admin":
            query = query.where(Booking.user_id == current_user.id)

        result = await session.execute(query)
        bookings = result.scalars().unique().all()

        return [BookingResponse.model_validate(b) for b in bookings]
