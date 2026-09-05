from app.application.ports.user_repository import UserRepositoryPort
from app.core.security import verify_password, create_access_token

class AuthUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        
        token = create_access_token(data={"sub": str(user.id)})
        return token