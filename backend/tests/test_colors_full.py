import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.models.car import Car

@pytest.mark.asyncio
async def test_car_catalog_has_factory_colors_for_all(client: AsyncClient):
    """
    Verifica que TODOS los coches del catálogo público tengan un color de fábrica.
    """
    response = await client.get("/api/v1/cars/")
    assert response.status_code == 200
    cars = response.json()
    assert len(cars) > 0
    for car in cars:
        assert "color_fabrica" in car
        assert car["color_fabrica"] is not None
        assert len(car["color_fabrica"]) > 0

@pytest.mark.asyncio
async def test_unregistered_user_cannot_update_color(client: AsyncClient):
    """
    Verifica que un usuario no autenticado obtenga 401/403 al intentar cambiar un color.
    """
    car_id = 1
    response = await client.patch(
        f"/api/v1/favorites/{car_id}/color",
        json={"selected_color": "Neon"}
    )
    # Debe fallar por falta de token
    assert response.status_code in [401, 403]

@pytest.mark.asyncio
async def test_registered_user_full_color_flow(client: AsyncClient, db_session: Session, user_token_headers: dict):
    """
    Flujo completo: Ver color fábrica -> Añadir a favoritos -> Cambiar color -> Verificar.
    """
    # 1. Ver un coche y su color de fábrica
    car_response = await client.get("/api/v1/cars/")
    first_car = car_response.json()[0]
    car_id = first_car["id"]
    original_color = first_car["color_fabrica"]
    
    # 2. Añadirlo a favoritos (sin especificar color al principio)
    add_resp = await client.post(
        "/api/v1/favorites/",
        json={"car_id": car_id},
        headers=user_token_headers
    )
    assert add_resp.status_code == 201
    assert add_resp.json()["selected_color"] is None # Default
    
    # 3. Personalizar el color
    custom_color = "Verde Alienígena"
    patch_resp = await client.patch(
        f"/api/v1/favorites/{car_id}/color",
        json={"selected_color": custom_color},
        headers=user_token_headers
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["selected_color"] == custom_color
    
    # 4. Verificar que el color de fábrica del coche sigue siendo el mismo e intacto
    assert patch_resp.json()["car"]["color_fabrica"] == original_color
