from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Base con atributos comunes
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


# DTO de entrada para creación de usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


# DTO de entrada para actualización
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    password: str | None = Field(None, min_length=8, max_length=100)


# DTO de salida (Respuesta pública)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)