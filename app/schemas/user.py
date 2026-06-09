from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    login: str
    password: str
    full_name: str
    email: str


class UserLogin(BaseModel):
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


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
