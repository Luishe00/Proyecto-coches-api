from typing import List, Optional
from app.repositories.car_repository import ICarRepository
from app.schemas.car import CarCreate, CarUpdate, CarFilter
from app.domain import entities as domain
from app.core.exceptions import EntityNotFoundError


def get_car(repository: ICarRepository, car_id: int) -> domain.Car:
    car = repository.get_by_id(car_id)
    if not car:
        raise EntityNotFoundError(detail="Car not found")
    return car


def get_cars(repository: ICarRepository, filters: CarFilter, skip: int = 0, limit: int = 100) -> List[domain.Car]:
    return repository.get_all(filters, skip=skip, limit=limit)


def create_car(repository: ICarRepository, car_in: CarCreate) -> domain.Car:
    return repository.create(car_in)


def update_car(repository: ICarRepository, car_id: int, car_in: CarUpdate) -> domain.Car:
    # Primero verificamos que exista lanzando excepción si no
    get_car(repository, car_id)
    return repository.update(car_id, car_in)


def delete_car(repository: ICarRepository, car_id: int) -> domain.Car:
    # Verificamos que exista
    get_car(repository, car_id)
    return repository.delete(car_id)
