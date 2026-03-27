import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import AppException
from app.db.session import engine, Base
from app.models.favorite import Favorite
from app.routers import auth, cars, favorites


# Create tables if they don't exist
# In production, use migrations (alembic) instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Asegurar que el directorio estático existe
os.makedirs("app/infrastructure/static/uploads/cars", exist_ok=True)

# Montar ruta estática para servir imágenes
app.mount("/static", StaticFiles(directory="app/infrastructure/static"), name="static")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    headers = {}
    if exc.status_code == 401:
        headers["WWW-Authenticate"] = "Bearer"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers
    )


app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(cars.router, prefix=f"{settings.API_V1_STR}/cars", tags=["cars"])
app.include_router(favorites.router, prefix=f"{settings.API_V1_STR}/favorites", tags=["favorites"])
