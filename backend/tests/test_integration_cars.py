import pytest
from sqlalchemy.orm import Session
from app.services import car_service
from app.repositories.car_repository import SQLAlchemyCarRepository
from app.schemas.car import CarCreate, CarFilter

def test_integration_get_all_cars_no_filters(db_session: Session):
    """Verifica que se recuperan todos los coches sembrados en conftest."""
    repo = SQLAlchemyCarRepository(db_session)
    # Toyota y BMW ya están sembrados en conftest.py
    results = car_service.get_cars(repo, CarFilter())
    
    assert len(results) >= 2
    marcas = [c.marca for c in results]
    assert "Toyota" in marcas
    assert "BMW" in marcas

def test_integration_filter_by_marca(db_session: Session):
    """Prueba de equivalencia: Filtrar por marca existente."""
    repo = SQLAlchemyCarRepository(db_session)
    filters = CarFilter(marca="Toyota")
    results = car_service.get_cars(repo, filters)
    
    assert len(results) == 1
    assert results[0].marca == "Toyota"

def test_integration_pagination(db_session: Session):
    """Verifica el funcionamiento de skip y limit sobre datos reales."""
    repo = SQLAlchemyCarRepository(db_session)
    
    # Obtener el primero
    page1 = car_service.get_cars(repo, CarFilter(), skip=0, limit=1)
    assert len(page1) == 1
    
    # Obtener el segundo
    page2 = car_service.get_cars(repo, CarFilter(), skip=1, limit=1)
    assert len(page2) == 1
    assert page1[0].id != page2[0].id

def test_integration_create_and_get(db_session: Session):
    """Validación de persistencia: Crear y recuperar sin mocks."""
    repo = SQLAlchemyCarRepository(db_session)
    car_in = CarCreate(
        marca="Audi", 
        modelo="A3", 
        anio_fabricacion=2022, 
        cv=150, 
        peso=1400, 
        velocidad_max=220, 
        precio=35000, 
        color_fabrica="Gris"
    )
    
    # Crear
    created_car = car_service.create_car(repo, car_in)
    assert created_car.id is not None
    
    # Recuperar
    retrieved_car = car_service.get_car(repo, created_car.id)
    assert retrieved_car.marca == "Audi"
    assert retrieved_car.modelo == "A3"
