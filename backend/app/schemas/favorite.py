from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.car import CarResponse

class FavoriteCreate(BaseModel):
    car_id: int
    selected_color: Optional[str] = None

class FavoriteColorUpdate(BaseModel):
    selected_color: str

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    created_at: datetime
    car: CarResponse
    selected_color: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
