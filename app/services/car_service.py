from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdate, CarFilter

def get_car(db: Session, car_id: int) -> Car:
    return db.query(Car).filter(Car.id == car_id).first()


def get_cars(db: Session, filters: CarFilter, skip: int = 0, limit: int = 100) -> list[Car]:
    query = db.query(Car)

    if filters.marca:
        query = query.filter(Car.marca.ilike(f"%{filters.marca}%"))
    if filters.modelo:
        query = query.filter(Car.modelo.ilike(f"%{filters.modelo}%"))
    if filters.anio_min is not None:
        query = query.filter(Car.anio_fabricacion >= filters.anio_min)
    if filters.anio_max is not None:
        query = query.filter(Car.anio_fabricacion <= filters.anio_max)
    if filters.precio_max is not None:
        query = query.filter(Car.precio <= filters.precio_max)
    if filters.velocidad_min is not None:
        query = query.filter(Car.velocidad_max >= filters.velocidad_min)

    return query.offset(skip).limit(limit).all()


def create_car(db: Session, car: CarCreate) -> Car:
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, db_car: Car, car: CarUpdate) -> Car:
    update_data = car.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_car, key, value)
    
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, db_car: Car) -> Car:
    db.delete(db_car)
    db.commit()
    return db_car
