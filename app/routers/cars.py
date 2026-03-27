from typing import List
from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.car import CarResponse as Car, CarCreate, CarUpdate, CarFilter
from app.services import car_service, auth_service
from app.services.car_image_service import CarImageService
from app.repositories.car_repository import ICarRepository, SQLAlchemyCarRepository
from app.domain.entities import User

router = APIRouter()

def get_car_repository(db: Session = Depends(get_db)) -> ICarRepository:
    return SQLAlchemyCarRepository(db)

@router.get("/", response_model=List[Car])
def read_cars(
    filters: CarFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Retrieve cars with advanced filtering.
    """
    return car_service.get_cars(repository, filters, skip=skip, limit=limit)

@router.get("/{car_id}", response_model=Car)
def read_car(
    car_id: int,
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Get a specific car by ID.
    """
    return car_service.get_car(repository, car_id)

@router.post("/", response_model=Car, status_code=status.HTTP_201_CREATED)
def create_car(
    car_in: CarCreate,
    current_user: User = Depends(auth_service.get_current_active_superadmin),
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Create new car. Requires 'superadmin' role.
    """
    return car_service.create_car(repository, car_in)

@router.put("/{car_id}", response_model=Car)
def update_car(
    car_id: int,
    car_in: CarUpdate,
    current_user: User = Depends(auth_service.get_current_active_superadmin),
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Update a car. Requires 'superadmin' role.
    """
    return car_service.update_car(repository, car_id, car_in)

@router.delete("/{car_id}", response_model=Car)
def delete_car(
    car_id: int,
    current_user: User = Depends(auth_service.get_current_active_superadmin),
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Delete a car. Requires 'superadmin' role.
    """
    return car_service.delete_car(repository, car_id)


@router.post("/{car_id}/image", response_model=Car)
def upload_car_image(
    car_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(auth_service.get_current_active_superadmin),
    repository: ICarRepository = Depends(get_car_repository)
):
    """
    Subir y asignar una imagen al coche. (Solo Superadmin)
    """
    # 1. Aseguramos que el coche existe (get_car lanza excepción si no)
    car_service.get_car(repository, car_id)
    
    # 2. Guardamos la imagen y obtenemos URL
    image_url = CarImageService.save_image(file)
    
    # 3. Actualizamos el coche
    car_update = CarUpdate(image_url=image_url)
    return car_service.update_car(repository, car_id, car_update)
