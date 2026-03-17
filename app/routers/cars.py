from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.car import CarCreate, CarUpdate, CarResponse, CarFilter
from app.schemas.user import UserOut
from app.services import car_service, auth_service

router = APIRouter()


@router.get("/", response_model=List[CarResponse])
def read_cars(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    filters: CarFilter = Depends()
) -> Any:
    """
    Retrieve cars with advanced filtering.
    """
    cars = car_service.get_cars(db, filters=filters, skip=skip, limit=limit)
    return cars


@router.post("/", response_model=CarResponse)
def create_car(
    *,
    db: Session = Depends(get_db),
    car_in: CarCreate,
    current_user: UserOut = Depends(auth_service.get_current_superadmin_user)
) -> Any:
    """
    Create new car. Requires 'superadmin' role.
    """
    car = car_service.create_car(db=db, car=car_in)
    return car


@router.get("/{car_id}", response_model=CarResponse)
def read_car(
    *,
    db: Session = Depends(get_db),
    car_id: int,
) -> Any:
    """
    Get car by ID.
    """
    car = car_service.get_car(db=db, car_id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    *,
    db: Session = Depends(get_db),
    car_id: int,
    car_in: CarUpdate,
    current_user: UserOut = Depends(auth_service.get_current_superadmin_user)
) -> Any:
    """
    Update a car. Requires 'superadmin' role.
    """
    car = car_service.get_car(db=db, car_id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car = car_service.update_car(db=db, db_car=car, car=car_in)
    return car


@router.delete("/{car_id}", response_model=CarResponse)
def delete_car(
    *,
    db: Session = Depends(get_db),
    car_id: int,
    current_user: UserOut = Depends(auth_service.get_current_superadmin_user)
) -> Any:
    """
    Delete a car. Requires 'superadmin' role.
    """
    car = car_service.get_car(db=db, car_id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car = car_service.delete_car(db=db, db_car=car)
    return car
