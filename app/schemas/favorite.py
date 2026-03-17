from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.car import CarResponse

class FavoriteCreate(BaseModel):
    car_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    created_at: datetime
    car: CarResponse
    
    model_config = ConfigDict(from_attributes=True)
