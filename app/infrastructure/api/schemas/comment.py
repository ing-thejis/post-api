from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.infrastructure.api.schemas.user import UserResponse


# Base con atributos comunes
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


# DTO de entrada para crear comentario
class CommentCreate(CommentBase):
    pass


# DTO de entrada para actualizar comentario
class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


# DTO de salida para comentarios
class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    author: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)