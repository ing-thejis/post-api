from typing import Optional
from sqlalchemy.orm import Session
from app.domain.models.user import User
from app.application.ports.user_repository import UserRepositoryPort
from app.infrastructure.database.models import UserModel # Modelo SQLAlchemy

class SQLAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active
        )

    def save(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.id = db_user.id
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active
        )