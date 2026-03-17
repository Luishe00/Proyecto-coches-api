from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.car import Car
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    *,
    db: Session = Depends(get_db),
    favorite_in: FavoriteCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Añade un coche a favoritos para el usuario autenticado.
    """
    # Verificar que el coche existe
    car = db.query(Car).filter(Car.id == favorite_in.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="El coche no existe.")
    
    # Crear el favorito
    favorite = Favorite(user_id=current_user.id, car_id=favorite_in.car_id)
    db.add(favorite)
    try:
        db.commit()
        db.refresh(favorite)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Este coche ya está en tus favoritos.")
    
    return favorite


@router.get("/", response_model=List[FavoriteResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Lista todos los coches favoritos del usuario autenticado.
    """
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    return favorites


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    *,
    db: Session = Depends(get_db),
    car_id: int,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Elimina un coche de los favoritos del usuario autenticado.
    """
    favorite = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.car_id == car_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="El coche no está en tus favoritos.")
    
    db.delete(favorite)
    db.commit()
    return None
