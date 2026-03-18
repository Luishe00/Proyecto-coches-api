import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.models.car import Car
from app.models.favorite import Favorite

@pytest.mark.asyncio
async def test_add_favorite_success(client: AsyncClient, db_session: Session, user_token_headers: dict):
    # Primero creamos un coche para añadirlo a favoritos
    car = Car(
        marca="Test",
        modelo="Favorite",
        anio_fabricacion=2024,
        cv=150,
        peso=1200.0,
        velocidad_max=200,
        precio=25000.0,
        color_fabrica="Blanco"
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)

    response = await client.post(
        "/api/v1/favorites/",
        json={"car_id": car.id},
        headers=user_token_headers
    )
    assert response.status_code == 201
    content = response.json()
    assert content["car_id"] == car.id

@pytest.mark.asyncio
async def test_add_favorite_non_existent_car(client: AsyncClient, user_token_headers: dict):
    response = await client.post(
        "/api/v1/favorites/",
        json={"car_id": 99999},
        headers=user_token_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "El coche no existe."

@pytest.mark.asyncio
async def test_add_favorite_duplicate(client: AsyncClient, db_session: Session, user_token_headers: dict):
    # Creamos un coche
    car = Car(
        marca="Test",
        modelo="Duplicate",
        anio_fabricacion=2024,
        cv=150,
        peso=1200.0,
        velocidad_max=200,
        precio=25000.0,
        color_fabrica="Blanco"
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)

    # Añadimos por primera vez
    await client.post(
        "/api/v1/favorites/",
        json={"car_id": car.id},
        headers=user_token_headers
    )
    
    # Intentamos añadir de nuevo
    response = await client.post(
        "/api/v1/favorites/",
        json={"car_id": car.id},
        headers=user_token_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Este coche ya está en tus favoritos."

@pytest.mark.asyncio
async def test_get_favorites(client: AsyncClient, user_token_headers: dict):
    response = await client.get(
        "/api/v1/favorites/",
        headers=user_token_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_remove_favorite(client: AsyncClient, db_session: Session, user_token_headers: dict):
    # Creamos un coche y lo añadimos a favoritos
    car = Car(
        marca="Test",
        modelo="ToRemove",
        anio_fabricacion=2024,
        cv=150,
        peso=1200.0,
        velocidad_max=200,
        precio=25000.0,
        color_fabrica="Blanco"
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)

    await client.post(
        "/api/v1/favorites/",
        json={"car_id": car.id},
        headers=user_token_headers
    )

    # Eliminamos de favoritos
    response = await client.delete(
        f"/api/v1/favorites/{car.id}",
        headers=user_token_headers
    )
    assert response.status_code == 204

    # Verificamos que ya no está
    resp_get = await client.get(
        "/api/v1/favorites/",
        headers=user_token_headers
    )
    favorites = resp_get.json()
    assert all(f["car_id"] != car.id for f in favorites)
