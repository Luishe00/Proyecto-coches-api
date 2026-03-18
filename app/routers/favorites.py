from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.services import favorite_service
from app.services.auth_service import get_current_active_user
from app.repositories.favorite_repository import IFavoriteRepository, SQLAlchemyFavoriteRepository
from app.domain.entities import User

router = APIRouter()

def get_favorite_repository(db: Session = Depends(get_db)) -> IFavoriteRepository:
    return SQLAlchemyFavoriteRepository(db)

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    favorite_in: FavoriteCreate,
    repository: IFavoriteRepository = Depends(get_favorite_repository),
    current_user: User = Depends(get_current_active_user),
):
    """
    Añade un coche a favoritos para el usuario autenticado.
    """
    return favorite_service.create_favorite(
        repository, user_id=current_user.id, car_id=favorite_in.car_id
    )

@router.get("/", response_model=List[FavoriteResponse])
def get_favorites(
    repository: IFavoriteRepository = Depends(get_favorite_repository),
    current_user: User = Depends(get_current_active_user),
):
    """
    Lista todos los coches favoritos del usuario autenticado.
    """
    return favorite_service.get_user_favorites(repository, user_id=current_user.id)

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    car_id: int,
    repository: IFavoriteRepository = Depends(get_favorite_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a car from favorites.
    """
    favorite_service.remove_favorite(repository, user_id=current_user.id, car_id=car_id)
    return None
