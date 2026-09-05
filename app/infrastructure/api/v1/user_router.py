from fastapi import APIRouter, Depends
from app.domain.models.user import User
from app.infrastructure.api.dependencies import get_current_user
from app.infrastructure.api.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint protegido: Solo accesible con un Bearer Token válido.
    """
    return current_user
