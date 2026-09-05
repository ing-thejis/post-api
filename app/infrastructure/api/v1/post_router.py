from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.domain.models.user import User
from app.application.use_cases.post_use_case import PostUseCase
from app.infrastructure.api.dependencies import get_current_user, get_post_use_case
from app.infrastructure.api.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    current_user: User = Depends(get_current_user),
    post_use_case: PostUseCase = Depends(get_post_use_case)
):
    """Crea una nueva publicación vinculada al usuario autenticado."""
    return post_use_case.create_post(
        title=post_in.title,
        content=post_in.content,
        author_id=current_user.id
    )


@router.get("/", response_model=List[PostResponse])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    post_use_case: PostUseCase = Depends(get_post_use_case)
):
    """Obtiene una lista paginada de publicaciones (público)."""
    return post_use_case.list_posts(skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    post_use_case: PostUseCase = Depends(get_post_use_case)
):
    """Obtiene una publicación específica por su ID."""
    try:
        return post_use_case.get_post(post_id=post_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_user),
    post_use_case: PostUseCase = Depends(get_post_use_case)
):
    """Actualiza una publicación. Solo el autor puede realizar esta acción."""
    try:
        return post_use_case.update_post(
            post_id=post_id,
            user_id=current_user.id,
            title=post_in.title,
            content=post_in.content
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_use_case: PostUseCase = Depends(get_post_use_case)
):
    """Elimina una publicación. Solo el autor puede realizar esta acción."""
    try:
        post_use_case.delete_post(post_id=post_id, user_id=current_user.id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))