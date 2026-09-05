from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env en el entorno del sistema
load_dotenv()



class Settings(BaseSettings):
    PROJECT_NAME: str = "API Rest using FastAPI Hexagonal Architecture"
    API_V1_STR: str = "/api/v1"
    
    # JWT Configuration
    SECRET_KEY: str = os.environ.get("JWT_SECRET")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # Database
    DATABASE_URL: str = os.environ.get("DB_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()