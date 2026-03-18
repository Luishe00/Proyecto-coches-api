from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    superadmin = "superadmin"

@dataclass
class Car:
    marca: str
    modelo: str
    anio_fabricacion: int
    cv: int
    peso: float
    velocidad_max: int
    precio: float
    color_fabrica: str
    id: Optional[int] = None

@dataclass
class User:
    username: str
    hashed_password: str
    role: RoleEnum = RoleEnum.user
    id: Optional[int] = None

@dataclass
class Favorite:
    user_id: int
    car_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    car: Optional[Car] = None
    selected_color: Optional[str] = None
