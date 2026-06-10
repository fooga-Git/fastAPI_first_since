from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    login: str
    full_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class SetRoleRequest(BaseModel):
    user_id: int
    role: Literal['employee', 'admin']
