import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException

# Definir la ruta base relativa desde el backend
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "infrastructure", "static", "uploads", "cars")

class CarImageService:
    ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp"}

    @staticmethod
    def save_image(file: UploadFile) -> str:
        if file.content_type not in CarImageService.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Solo se permiten imágenes (JPEG, PNG, WEBP).")

        os.makedirs(STATIC_DIR, exist_ok=True)
        
        # Generar nombre único
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(STATIC_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Retornar la URL estática
        return f"/static/uploads/cars/{filename}"
