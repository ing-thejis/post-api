from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.infrastructure.api.schemas.user import UserResponse
from app.infrastructure.api.schemas.comment import CommentResponse


# Base con atributos comunes
class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=5)


# DTO de entrada para creación de publicación
class PostCreate(PostBase):
    pass


# DTO de entrada para actualización parcial
class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    content: str | None = Field(None, min_length=5)


# DTO de salida simple
class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    author: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


# DTO de salida detallado (incluye lista de comentarios)
class PostDetailResponse(PostResponse):
    comments: list[CommentResponse] = []

    model_config = ConfigDict(from_attributes=True)