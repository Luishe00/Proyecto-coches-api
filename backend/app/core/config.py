import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Car Catalog API"
    API_V1_STR: str = "/api/v1"
    
    # Pydantic buscará estas variables en el archivo .env automáticamente
    SECRET_KEY: str = "super_secret_key_for_jwt_auth_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = "sqlite:///./cars.db"

    # Esta es la nueva forma de configurar en Pydantic V2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore" # Esto silencia el error de "Extra inputs"
    )

settings = Settings()