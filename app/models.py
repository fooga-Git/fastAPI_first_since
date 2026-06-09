from datetime import date as date_type
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UniqueConstraint

from app.core.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class User(BaseModel):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(225), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="employee")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")


class Room(BaseModel):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    capacity: Mapped[int] = mapped_column(nullable=False)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)
    bookings: Mapped[List["Booking"]] = relationship(back_populates="room")


class Slot(BaseModel):
    __tablename__ = "slots"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    time_range: Mapped[str] = mapped_column(String(20), nullable=False)
    is_night: Mapped[bool] = mapped_column(default=False)
    number: Mapped[int] = mapped_column(nullable=False)
    bookings: Mapped[List["Booking"]] = relationship(back_populates="slot")


class Booking(BaseModel):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    date: Mapped[date_type] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")

    user: Mapped["User"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="bookings")
    slot: Mapped["Slot"] = relationship(back_populates="bookings")

    __table_args__ = (UniqueConstraint(
        "room_id",
        "slot_id",
        "date",
        name="unique_booking"),
    )
