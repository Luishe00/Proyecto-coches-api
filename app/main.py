from fastapi import FastAPI

from app.core.config import settings
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

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(cars.router, prefix=f"{settings.API_V1_STR}/cars", tags=["cars"])
app.include_router(favorites.router, prefix=f"{settings.API_V1_STR}/favorites", tags=["favorites"])
