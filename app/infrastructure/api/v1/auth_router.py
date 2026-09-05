from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.application.use_cases.auth_use_case import AuthUseCase
from app.infrastructure.api.dependencies import get_auth_use_case

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthUseCase = Depends(get_auth_use_case)
):
    try:
        token = auth_use_case.authenticate_user(form_data.username, form_data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )