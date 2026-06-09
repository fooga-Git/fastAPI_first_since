from typing import Literal

from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    name: str
    capacity: int
    room_type: Literal["coworking", "podcast"]


class RoomUpdate(BaseModel):
    capacity: int | None = None
    room_type: Literal["coworking", "podcast"] | None = None


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    room_type: str
    model_config = ConfigDict(from_attributes=True)
