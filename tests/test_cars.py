import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_cars(client: AsyncClient):
    """
    Verificar que se listan los coches (acceso público/sin token requerido).
    """
    response = await client.get("/api/v1/cars/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # Seeded in conftest

@pytest.mark.asyncio
async def test_filter_cars_by_brand(client: AsyncClient):
    """
    Verificar el filtrado por marca.
    """
    response = await client.get("/api/v1/cars/?marca=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["marca"] == "Toyota"
    assert data[0]["modelo"] == "Corolla"

@pytest.mark.asyncio
async def test_normal_user_cannot_create_car(client: AsyncClient, user_token_headers: dict):
    """
    Verificar que un usuario normal no puede crear coches (RBAC).
    """
    car_data = {
        "marca": "Audi",
        "modelo": "A4",
        "anio_fabricacion": 2022,
        "cv": 190,
        "peso": 1500,
        "velocidad_max": 240,
        "precio": 45000
    }
    response = await client.post(
        "/api/v1/cars/",
        headers=user_token_headers,
        json=car_data
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "The user doesn't have enough privileges"

@pytest.mark.asyncio
async def test_superadmin_can_create_car(client: AsyncClient, superadmin_token_headers: dict):
    """
    Verificar que un superadmin sí puede crear coches.
    """
    car_data = {
        "marca": "Tesla",
        "modelo": "Model 3",
        "anio_fabricacion": 2023,
        "cv": 400,
        "peso": 1800,
        "velocidad_max": 250,
        "precio": 50000
    }
    response = await client.post(
        "/api/v1/cars/",
        headers=superadmin_token_headers,
        json=car_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == "Tesla"
    assert "id" in data
