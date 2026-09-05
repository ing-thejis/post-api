from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.domain.models.user import User
from app.application.use_cases.comment_use_case import CommentUseCase
from app.infrastructure.api.dependencies import get_current_user, get_comment_use_case
from app.infrastructure.api.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(tags=["Comments"])


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    post_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    comment_use_case: CommentUseCase = Depends(get_comment_use_case)
):
    """Añade un comentario a una publicación específica."""
    try:
        return comment_use_case.add_comment(
            post_id=post_id,
            author_id=current_user.id,
            content=comment_in.content
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def list_comments_by_post(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    comment_use_case: CommentUseCase = Depends(get_comment_use_case)
):
    """Listar todos los comentarios de una publicación."""
    try:
        return comment_use_case.list_comments_by_post(post_id=post_id, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    comment_use_case: CommentUseCase = Depends(get_comment_use_case)
):
    """Elimina un comentario. Solo el autor del comentario puede realizar esta acción."""
    try:
        comment_use_case.delete_comment(comment_id=comment_id, user_id=current_user.id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))