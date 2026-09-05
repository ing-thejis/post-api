from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Engine para SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Requerido solo para SQLite
    echo=False  # Cambiar a True para ver las consultas SQL generadas en la consola
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa moderna (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass