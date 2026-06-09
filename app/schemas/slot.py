from pydantic import BaseModel, ConfigDict


class SlotResponse(BaseModel):
    number: int
    room_id: int
    time_range: str
    is_night: bool

    model_config = ConfigDict(from_attributes=True)
