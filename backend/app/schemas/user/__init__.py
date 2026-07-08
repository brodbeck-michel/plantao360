from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(default="CONSULTA", max_length=20)


class UserUpdateDTO(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    email: str | None = Field(None, min_length=1, max_length=255)
    password: str | None = Field(None, min_length=6, max_length=128)
    role: str | None = Field(None, max_length=20)
    active: bool | None = None


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    role: str
    active: bool
    last_login: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class LoginRequestDTO(BaseModel):
    email: str
    password: str


class ChangePasswordDTO(BaseModel):
    password: str = Field(..., min_length=6, max_length=128)


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDTO
