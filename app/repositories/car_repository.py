from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.car import Car as DBModel
from app.domain import entities as domain
from app.schemas.car import CarCreate, CarUpdate, CarFilter

class ICarRepository(ABC):
    @abstractmethod
    def get_by_id(self, car_id: int) -> Optional[domain.Car]:
        pass

    @abstractmethod
    def get_all(self, filters: CarFilter, skip: int = 0, limit: int = 100) -> List[domain.Car]:
        pass

    @abstractmethod
    def create(self, car_in: CarCreate) -> domain.Car:
        pass

    @abstractmethod
    def update(self, db_car_id: int, car_in: CarUpdate) -> domain.Car:
        pass

    @abstractmethod
    def delete(self, car_id: int) -> domain.Car:
        pass

class SQLAlchemyCarRepository(ICarRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_car: DBModel) -> Optional[domain.Car]:
        if not db_car:
            return None
        return domain.Car(
            id=db_car.id,
            marca=db_car.marca,
            modelo=db_car.modelo,
            anio_fabricacion=db_car.anio_fabricacion,
            cv=db_car.cv,
            peso=db_car.peso,
            velocidad_max=db_car.velocidad_max,
            precio=db_car.precio,
            color_fabrica=db_car.color_fabrica,
            image_url=db_car.image_url
        )

    def get_by_id(self, car_id: int) -> Optional[domain.Car]:
        db_car = self.db.query(DBModel).filter(DBModel.id == car_id).first()
        return self._to_domain(db_car)

    def get_all(self, filters: CarFilter, skip: int = 0, limit: int = 100) -> List[domain.Car]:
        query = self.db.query(DBModel)
        if filters.marca:
            query = query.filter(DBModel.marca.ilike(f"%{filters.marca}%"))
        if filters.modelo:
            query = query.filter(DBModel.modelo.ilike(f"%{filters.modelo}%"))
        if filters.anio_min is not None:
            query = query.filter(DBModel.anio_fabricacion >= filters.anio_min)
        if filters.anio_max is not None:
            query = query.filter(DBModel.anio_fabricacion <= filters.anio_max)
        if filters.precio_max is not None:
            query = query.filter(DBModel.precio <= filters.precio_max)
        if filters.velocidad_min is not None:
            query = query.filter(DBModel.velocidad_max >= filters.velocidad_min)
        
        db_cars = query.offset(skip).limit(limit).all()
        return [self._to_domain(car) for car in db_cars]

    def create(self, car_in: CarCreate) -> domain.Car:
        db_car = DBModel(**car_in.model_dump())
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return self._to_domain(db_car)

    def update(self, db_car_id: int, car_in: CarUpdate) -> domain.Car:
        db_car = self.db.query(DBModel).filter(DBModel.id == db_car_id).first()
        update_data = car_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_car, key, value)
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return self._to_domain(db_car)

    def delete(self, car_id: int) -> domain.Car:
        db_car = self.db.query(DBModel).filter(DBModel.id == car_id).first()
        car_domain = self._to_domain(db_car)
        self.db.delete(db_car)
        self.db.commit()
        return car_domain
