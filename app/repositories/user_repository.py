from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User as DBModel
from app.domain import entities as domain

class IUserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[domain.User]:
        pass

    @abstractmethod
    def create(self, username: str, hashed_password: str, role: domain.RoleEnum) -> domain.User:
        pass

class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_user: DBModel) -> Optional[domain.User]:
        if not db_user:
            return None
        return domain.User(
            id=db_user.id,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            role=domain.RoleEnum(db_user.role.value)
        )

    def get_by_username(self, username: str) -> Optional[domain.User]:
        db_user = self.db.query(DBModel).filter(DBModel.username == username).first()
        return self._to_domain(db_user)

    def create(self, username: str, hashed_password: str, role: domain.RoleEnum) -> domain.User:
        db_user = DBModel(
            username=username,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)
