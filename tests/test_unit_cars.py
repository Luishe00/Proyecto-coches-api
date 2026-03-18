import pytest
from unittest.mock import MagicMock
from app.services import car_service
from app.repositories.car_repository import ICarRepository
from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdate, CarFilter
from app.core.exceptions import EntityNotFoundError

def test_get_car_unit():
    """
    Test unitario puro del servicio: No necesita Base de Datos.
    Usa un Mock para simular el Repositorio.
    """
    # 1. Arrange: Preparamos el mock y el dato de prueba
    mock_repo = MagicMock(spec=ICarRepository)
    fake_car = Car(id=99, marca="Tesla", modelo="Model S", precio=100000, color_fabrica="Blanco")
    mock_repo.get_by_id.return_value = fake_car

    # 2. Act: Llamamos al servicio pasarle el mock
    result = car_service.get_car(repository=mock_repo, car_id=99)

    # 3. Assert: Verificamos que el servicio haga lo que debe
    assert result.marca == "Tesla"
    assert result.id == 99
    # Verificamos que se llamó al repositorio con el ID correcto
    mock_repo.get_by_id.assert_called_once_with(99)

def test_get_car_not_found_unit():
    """
    Verifica que el servicio lance la excepción correcta si el repo devuelve None.
    """
    mock_repo = MagicMock(spec=ICarRepository)
    mock_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc:
        car_service.get_car(repository=mock_repo, car_id=999)
    
    assert exc.value.detail == "Car not found"

def test_create_car_unit():
    """
    Verifica la creación delegando en el repositorio.
    """
    mock_repo = MagicMock(spec=ICarRepository)
    car_in = CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=2022, cv=150, peso=1400, velocidad_max=210, precio=30000, color_fabrica="Azul")
    fake_car = Car(id=1, **car_in.model_dump())
    mock_repo.create.return_value = fake_car

    result = car_service.create_car(repository=mock_repo, car_in=car_in)

    assert result.marca == "Ford"
    mock_repo.create.assert_called_once_with(car_in)
