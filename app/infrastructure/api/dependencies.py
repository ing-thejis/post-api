from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.models.user import User
from app.infrastructure.database.session import SessionLocal

from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.sqlalchemy_post_repository import SQLAlchemyPostRepository
from app.infrastructure.repositories.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from app.application.use_cases.auth_use_case import AuthUseCase
from app.application.use_cases.user_use_case import UserUseCase
from app.application.use_cases.post_use_case import PostUseCase
from app.application.use_cases.comment_use_case import CommentUseCase

from app.infrastructure.api.schemas.auth import TokenPayload

# Define el endpoint desde donde los clientes obtienen el Token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# 1. Dependencia de Sesión de Base de Datos
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. Inyección de Repositorios y Casos de Uso
def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)

def get_auth_use_case(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> AuthUseCase:
    return AuthUseCase(user_repo=user_repo)

def get_user_use_case(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserUseCase:
    return UserUseCase(user_repo=user_repo)

# 3. Guardián de Seguridad / Obtener Usuario Autenticado Actual
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_id(user_id=int(token_data.sub))
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
        
    return user

# --- Repositorios ---
def get_post_repository(db: Session = Depends(get_db)) -> SQLAlchemyPostRepository:
    return SQLAlchemyPostRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> SQLAlchemyCommentRepository:
    return SQLAlchemyCommentRepository(db)


# --- Casos de Uso ---
def get_post_use_case(
    post_repo: SQLAlchemyPostRepository = Depends(get_post_repository)
) -> PostUseCase:
    return PostUseCase(post_repo=post_repo)

def get_comment_use_case(
    comment_repo: SQLAlchemyCommentRepository = Depends(get_comment_repository),
    post_repo: SQLAlchemyPostRepository = Depends(get_post_repository)
) -> CommentUseCase:
    return CommentUseCase(comment_repo=comment_repo, post_repo=post_repo)