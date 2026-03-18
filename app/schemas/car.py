from pydantic import BaseModel, Field, ConfigDict


class CarBase(BaseModel):
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=100)
    anio_fabricacion: int = Field(..., ge=1886, le=2027)
    cv: int = Field(..., gt=0)
    peso: float = Field(..., gt=0)
    velocidad_max: int = Field(..., gt=0)
    precio: float = Field(..., gt=0)
    color_fabrica: str = Field(..., min_length=2, max_length=50)


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    marca: str | None = Field(None, min_length=2, max_length=50)
    modelo: str | None = Field(None, min_length=1, max_length=100)
    anio_fabricacion: int | None = Field(None, ge=1886, le=2027)
    cv: int | None = Field(None, gt=0)
    peso: float | None = Field(None, gt=0)
    velocidad_max: int | None = Field(None, gt=0)
    precio: float | None = Field(None, gt=0)
    color_fabrica: str | None = Field(None, min_length=2, max_length=50)


class CarResponse(CarBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class CarFilter(BaseModel):
    marca: str | None = None
    modelo: str | None = None
    anio_min: int | None = None
    anio_max: int | None = None
    precio_max: float | None = None
    velocidad_min: int | None = None
    color_fabrica: str | None = None
