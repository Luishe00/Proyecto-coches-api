from pydantic import BaseModel, ConfigDict, Field
from app.models.user import RoleEnum
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str = Field(..., max_length=72) # Limitamos a 72 para evitar el error de bcrypt
    role: RoleEnum = RoleEnum.user

# Lo renombramos a UserOut para que coincida con lo que pide tu auth.py
class UserOut(UserBase):
    id: int
    role: RoleEnum

    # Usamos model_config que es el estándar actual de Pydantic V2
    model_config = ConfigDict(from_attributes=True)

# Añadimos estas clases que son fundamentales para el login
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None