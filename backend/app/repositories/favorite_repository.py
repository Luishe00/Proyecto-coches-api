from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.favorite import Favorite as DBModel
from app.models.car import Car as DBCar
from app.domain import entities as domain
from app.core.exceptions import ConflictError, EntityNotFoundError

class IFavoriteRepository(ABC):
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[domain.Favorite]:
        pass

    @abstractmethod
    def get_by_user_and_car(self, user_id: int, car_id: int) -> Optional[domain.Favorite]:
        pass

    @abstractmethod
    def create(self, user_id: int, car_id: int, selected_color: Optional[str] = None) -> domain.Favorite:
        pass

    @abstractmethod
    def update_color(self, favorite_id: int, selected_color: str) -> domain.Favorite:
        pass

    @abstractmethod
    def delete(self, favorite: domain.Favorite) -> None:
        pass

    @abstractmethod
    def car_exists(self, car_id: int) -> bool:
        pass

class SQLAlchemyFavoriteRepository(IFavoriteRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_fav: DBModel) -> Optional[domain.Favorite]:
        if not db_fav:
            return None
        
        car_domain = None
        if db_fav.car:
            car_domain = domain.Car(
                id=db_fav.car.id,
                marca=db_fav.car.marca,
                modelo=db_fav.car.modelo,
                anio_fabricacion=db_fav.car.anio_fabricacion,
                cv=db_fav.car.cv,
                peso=db_fav.car.peso,
                velocidad_max=db_fav.car.velocidad_max,
                precio=db_fav.car.precio,
                color_fabrica=db_fav.car.color_fabrica,
                image_url=db_fav.car.image_url,
            )

        return domain.Favorite(
            id=db_fav.id,
            user_id=db_fav.user_id,
            car_id=db_fav.car_id,
            created_at=db_fav.created_at,
            car=car_domain,
            selected_color=db_fav.selected_color
        )

    def get_by_user(self, user_id: int) -> List[domain.Favorite]:
        db_favs = self.db.query(DBModel).filter(DBModel.user_id == user_id).all()
        return [self._to_domain(fav) for fav in db_favs]

    def get_by_user_and_car(self, user_id: int, car_id: int) -> Optional[domain.Favorite]:
        db_fav = self.db.query(DBModel).filter(
            DBModel.user_id == user_id, 
            DBModel.car_id == car_id
        ).first()
        return self._to_domain(db_fav)

    def create(self, user_id: int, car_id: int, selected_color: Optional[str] = None) -> domain.Favorite:
        db_fav = DBModel(user_id=user_id, car_id=car_id, selected_color=selected_color)
        self.db.add(db_fav)
        try:
            self.db.commit()
            self.db.refresh(db_fav)
        except IntegrityError:
            self.db.rollback()
            raise ConflictError(detail="Este coche ya está en tus favoritos.")
        return self._to_domain(db_fav)

    def update_color(self, favorite_id: int, selected_color: str) -> domain.Favorite:
        db_fav = self.db.query(DBModel).filter(DBModel.id == favorite_id).first()
        if not db_fav:
            raise EntityNotFoundError(detail="Favorito no encontrado.")
        
        db_fav.selected_color = selected_color
        self.db.commit()
        self.db.refresh(db_fav)
        return self._to_domain(db_fav)

    def delete(self, favorite: domain.Favorite) -> None:
        db_fav = self.db.query(DBModel).filter(DBModel.id == favorite.id).first()
        if db_fav:
            self.db.delete(db_fav)
            self.db.commit()

    def car_exists(self, car_id: int) -> bool:
        return self.db.query(DBCar).filter(DBCar.id == car_id).first() is not None
