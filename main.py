from fastapi import FastAPI
from app.core.config import settings
from app.infrastructure.database.session import Base, engine
from app.infrastructure.database import models  # Carga los modelos para registrarlos en Base

from app.infrastructure.api.v1.auth_router import router as auth_router
from app.infrastructure.api.v1.user_router import router as user_router
from app.infrastructure.api.v1.post_router import router as post_router
from app.infrastructure.api.v1.comment_router import router as comment_router

# Crea automáticamente las tablas si no existen en SQLite
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Registro de Routers agrupados bajo el prefijo común /api/v1
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(post_router, prefix=settings.API_V1_STR)
app.include_router(comment_router, prefix=settings.API_V1_STR)

# Define a simple GET endpoint
@app.get("/")
def root():
    return {"message": "API Rest Hexagonal con FastAPI funcionando correctamente"}


