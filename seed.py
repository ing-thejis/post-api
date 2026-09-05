from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.application.use_cases.user_use_case import UserUseCase

def create_initial_users():
    db = SessionLocal()
    try:
        user_repo = SQLAlchemyUserRepository(db)
        user_use_case = UserUseCase(user_repo)

        users_to_create = [
            {"email": "admin@example.com", "username": "admin", "password": "adminpass123"},
            {"email": "user1@example.com", "username": "user1", "password": "userpass123"}
        ]

        for user_data in users_to_create:
            try:
                user = user_use_case.create_user(**user_data)
                print(f"Usuario creado exitosamente: {user.username} (ID: {user.id})")
            except ValueError as e:
                print(f"Omitido '{user_data['username']}': {e}")
                
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_users()