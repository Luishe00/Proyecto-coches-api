import pytest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile, HTTPException
from app.services.car_image_service import CarImageService
import io

@patch("app.services.car_image_service.os.makedirs")
@patch("app.services.car_image_service.shutil.copyfileobj")
@patch("app.services.car_image_service.uuid")
@patch("builtins.open")
def test_save_image_success(mock_open, mock_uuid, mock_copyfileobj, mock_makedirs):
    """Verifica que procese, cree directorios y retorne URL correcta aislando el FileSystem."""
    mock_uuid.uuid4.return_value.hex = "fakeuuid"
    
    # Simular objeto UploadFile válido
    file_bytes = b"fake_image_content"
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "my_car.jpeg"
    mock_file.file = io.BytesIO(file_bytes)
    
    result = CarImageService.save_image(mock_file)

    assert result == "/static/uploads/cars/fakeuuid.jpeg"
    mock_makedirs.assert_called_once()
    mock_open.assert_called_once()
    mock_copyfileobj.assert_called_once()

@patch("app.services.car_image_service.os.makedirs")
def test_save_image_invalid_type(mock_makedirs):
    """Verifica el rechazo inmediato (HTTPException 400) al pasar un formato no permitido."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "text/plain"
    mock_file.filename = "script.txt"
    
    with pytest.raises(HTTPException) as exc:
        CarImageService.save_image(mock_file)
        
    assert exc.value.status_code == 400
    assert "Solo se permiten imágenes" in exc.value.detail
    mock_makedirs.assert_not_called()

@patch("app.services.car_image_service.os.makedirs")
@patch("app.services.car_image_service.shutil.copyfileobj")
@patch("app.services.car_image_service.uuid")
@patch("builtins.open")
def test_save_image_no_extension(mock_open, mock_uuid, mock_copyfileobj, mock_makedirs):
    """Asegura que funcione y asigne 'jpg' por defecto si el archivo original no tiene extensión."""
    mock_uuid.uuid4.return_value.hex = "fakeuuid2"
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/png"
    # Archivo sin punto ni extensión
    mock_file.filename = "image_without_extension" 
    mock_file.file = io.BytesIO(b"fake_content")
    
    result = CarImageService.save_image(mock_file)

    assert result == "/static/uploads/cars/fakeuuid2.jpg"
    mock_makedirs.assert_called_once()
    mock_open.assert_called_once()
