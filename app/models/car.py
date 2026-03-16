from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50), index=True, nullable=False)
    modelo = Column(String(100), index=True, nullable=False)
    anio_fabricacion = Column(Integer, index=True, nullable=False)
    cv = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    velocidad_max = Column(Integer, nullable=False)
    precio = Column(Float, index=True, nullable=False)
