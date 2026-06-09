from typing import Literal
from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    room_id: int
    slot_number: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    date: date


class UserShort(BaseModel):
    id: int
    login: str
    full_name: str
    model_config = ConfigDict(from_attributes=True)


class RoomShort(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class SlotShort(BaseModel):
    number: int
    time_range: str
    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BaseModel):
    id: int
    status: str
    date: date
    slot: SlotShort
    room: RoomShort
    user: UserShort
    model_config = ConfigDict(from_attributes=True)
