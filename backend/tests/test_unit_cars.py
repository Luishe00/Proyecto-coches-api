import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock
from app.services import car_service
from app.repositories.car_repository import ICarRepository
from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdate, CarFilter
from app.core.exceptions import EntityNotFoundError

@pytest.fixture
def mock_repo():
    return MagicMock(spec=ICarRepository)

def test_get_car_success(mock_repo):
    """Prueba ruta de éxito al recuperar un coche."""
    fake_car = Car(id=1, marca="Ford", modelo="Focus", precio=20000, color_fabrica="Blanco")
    mock_repo.get_by_id.return_value = fake_car

    result = car_service.get_car(mock_repo, 1)

    assert result == fake_car
    mock_repo.get_by_id.assert_called_once_with(1)

def test_get_car_not_found(mock_repo):
    """Valida excepción al no encontrar un coche."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc:
        car_service.get_car(mock_repo, 999)
    assert exc.value.detail == "Car not found"

def test_get_cars(mock_repo):
    """Valida el listado de coches con filtros."""
    fake_list = [
        Car(id=1, marca="Ford", modelo="Focus", precio=20000, color_fabrica="Blanco"),
        Car(id=2, marca="Seat", modelo="Leon", precio=15000, color_fabrica="Rojo")
    ]
    mock_repo.get_all.return_value = fake_list
    filters = CarFilter(marca="Ford")

    result = car_service.get_cars(mock_repo, filters, skip=0, limit=10)

    assert result == fake_list
    mock_repo.get_all.assert_called_once_with(filters, skip=0, limit=10)

def test_create_car(mock_repo):
    """Valida la creación de un vehículo nuevo."""
    car_in = CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=2022, cv=150, peso=1400, velocidad_max=210, precio=30000, color_fabrica="Azul")
    fake_car = Car(id=1, **car_in.model_dump())
    mock_repo.create.return_value = fake_car

    result = car_service.create_car(mock_repo, car_in)

    assert result == fake_car
    mock_repo.create.assert_called_once_with(car_in)

def test_update_car_success(mock_repo):
    """Valida actualización exitosa de un coche existente."""
    existing_car = Car(id=1, marca="Ford", modelo="Focus", precio=20000, color_fabrica="Blanco")
    mock_repo.get_by_id.return_value = existing_car
    
    car_update = CarUpdate(precio=25000)
    updated_car = Car(id=1, marca="Ford", modelo="Focus", precio=25000, color_fabrica="Blanco")
    mock_repo.update.return_value = updated_car

    result = car_service.update_car(mock_repo, 1, car_update)

    assert result == updated_car
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once_with(1, car_update)

def test_update_car_not_found(mock_repo):
    """Valida rechazo de actualización cuando coche no existe."""
    mock_repo.get_by_id.return_value = None
    car_update = CarUpdate(precio=25000)

    with pytest.raises(EntityNotFoundError):
        car_service.update_car(mock_repo, 999, car_update)
    # verify update wasn't called
    mock_repo.update.assert_not_called()

def test_delete_car_success(mock_repo):
    """Valida eliminación exitosa de un coche."""
    existing_car = Car(id=1, marca="Ford", modelo="Focus", precio=20000, color_fabrica="Blanco")
    mock_repo.get_by_id.return_value = existing_car
    mock_repo.delete.return_value = existing_car

    result = car_service.delete_car(mock_repo, 1)

    assert result == existing_car
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.delete.assert_called_once_with(1)

def test_delete_car_not_found(mock_repo):
    """Valida rechazo de eliminación si no existe."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError):
        car_service.delete_car(mock_repo, 999)
    # verify delete wasn't called
    mock_repo.delete.assert_not_called()

# --- BLACK-BOX: Equivalence Classes ---
def test_car_create_year_valid():
    car = CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=1990, cv=100, peso=1200, velocidad_max=200, precio=10000, color_fabrica="Rojo")
    assert car.anio_fabricacion == 1990

def test_car_create_year_invalid_low():
    with pytest.raises(ValidationError):
        CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=1885, cv=100, peso=1200, velocidad_max=200, precio=10000, color_fabrica="Rojo")

def test_car_create_year_invalid_high():
    with pytest.raises(ValidationError):
        CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=2028, cv=100, peso=1200, velocidad_max=200, precio=10000, color_fabrica="Rojo")

def test_car_create_price_invalid_zero():
    with pytest.raises(ValidationError):
        CarCreate(marca="Ford", modelo="Focus", anio_fabricacion=2020, cv=100, peso=1200, velocidad_max=200, precio=0, color_fabrica="Rojo")

# --- BLACK-BOX: Decision Tables ---
@pytest.mark.parametrize("update_marca, update_precio", [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
])
def test_car_update_decision_table(update_marca, update_precio):
    update_data = {}
    if update_marca:
        update_data["marca"] = "Audi"
    if update_precio:
        update_data["precio"] = 30000
    
    car_update = CarUpdate(**update_data)
    
    if update_marca:
        assert car_update.marca == "Audi"
    else:
        assert car_update.marca is None
        
    if update_precio:
        assert car_update.precio == 30000
    else:
        assert car_update.precio is None
