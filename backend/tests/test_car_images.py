import pytest
from httpx import AsyncClient
import io

@pytest.mark.asyncio
async def test_superadmin_can_upload_car_image(client: AsyncClient, superadmin_token_headers: dict):
    """
    Verificar que el superadmin puede subir y asignar una imagen.
    """
    car_id = 1  # El test DB está 'seeded' con datos de prueba básicos desde conftest
    
    # Archivo falso de prueba
    file_content = b"fake_image_binary_data"
    files = {"file": ("test_car.jpg", io.BytesIO(file_content), "image/jpeg")}

    response = await client.post(
        f"/api/v1/cars/{car_id}/image",
        headers=superadmin_token_headers,
        files=files
    )

    assert response.status_code == 200
    data = response.json()
    assert "image_url" in data
    assert data["image_url"].startswith("/static/uploads/cars/")
    assert data["image_url"].endswith(".jpg")

@pytest.mark.asyncio
async def test_normal_user_cannot_upload_car_image(client: AsyncClient, user_token_headers: dict):
    """
    Verificar que un usuario normal sea rechazado (403 RBAC).
    """
    car_id = 1
    file_content = b"fake_image_binary_data"
    files = {"file": ("test_car.jpg", io.BytesIO(file_content), "image/jpeg")}

    response = await client.post(
        f"/api/v1/cars/{car_id}/image",
        headers=user_token_headers,
        files=files
    )

    assert response.status_code == 403
    assert "The user doesn't have enough privileges" in response.json()["detail"]

@pytest.mark.asyncio
async def test_upload_image_invalid_file_type(client: AsyncClient, superadmin_token_headers: dict):
    """
    Verificar que solo se acepten imágenes y se rechacen otros archivos (ej. TXT).
    """
    car_id = 1
    file_content = b"malicious_script_data"
    # Content-type modificado a text/plain
    files = {"file": ("script.txt", io.BytesIO(file_content), "text/plain")}

    response = await client.post(
        f"/api/v1/cars/{car_id}/image",
        headers=superadmin_token_headers,
        files=files
    )

    assert response.status_code == 400
    # Valida el mensaje devuelto por el CarImageService
    assert "Solo se permiten imágenes" in response.json()["detail"]
