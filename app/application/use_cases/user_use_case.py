from typing import Optional
from app.domain.models.user import User
from app.application.ports.user_repository import UserRepositoryPort
from app.core.security import get_password_hash


class UserUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def create_user(self, email: str, username: str, password: str) -> User:
        """Crea un nuevo usuario en el sistema validando duplicados."""
        # Validar si el email ya está registrado
        if self.user_repo.get_by_email(email):
            raise ValueError("El correo electrónico ya está registrado")

        # Generar hash seguro de la contraseña
        hashed_password = get_password_hash(password)

        new_user = User(
            id=None,
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=True,
        )

        return self.user_repo.save(new_user)

    def get_user_by_id(self, user_id: int) -> User:
        """Obtiene un usuario por su ID de manera segura."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user

    def update_user_profile(
        self, 
        user_id: int, 
        email: Optional[str] = None, 
        username: Optional[str] = None, 
        password: Optional[str] = None
    ) -> User:
        """Actualiza la información del usuario autenticado."""
        user = self.get_user_by_id(user_id)

        if email and email != user.email:
            if self.user_repo.get_by_email(email):
                raise ValueError("El correo electrónico ya está en uso")
            user.email = email

        if username:
            user.username = username

        if password:
            user.hashed_password = get_password_hash(password)

        return self.user_repo.save(user)