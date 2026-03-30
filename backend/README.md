# 🏎️ Car Catalog API - Arquitectura Hexagonal (100%)

Esta es una API REST profesional para un catálogo de coches de lujo, diseñada bajo los principios de **Arquitectura Hexagonal (Puertos y Adaptadores)**. Ofrece un sistema de roles (RBAC), gestión de favoritos y un núcleo de negocio 100% desacoplado.

## 🌟 Características Destacadas

- **Arquitectura Hexagonal Pura**: Separación estricta entre Dominio, Aplicación e Infraestructura.
- **RBAC (Role-Based Access Control)**: Diferenciación clara entre `superadmin` y `user`.
- **Catálogo de Coches**: CRUD completo para administradores y vistas de catálogo/favoritos para usuarios.
- **Base de Datos SQLite**: Sin dependencias externas pesadas, lista para funcionar.

## 🏗️ Estructura del Proyecto
- **Dominio (`app/domain`)**: Entidades de negocio (`Car`, `Favorite`, `User`). Zero dependencias externas.
- **Aplicación (`app/services`)**: Casos de uso como `favorite_service` que orquestan la lógica.
- **Infraestructura (`app/infrastructure/`)**: 
  - **FastAPI**: Adaptadores web, routers y esquemas Pydantic.
  - **SQLAlchemy**: Adaptadores de persistencia con mappers a entidades de dominio.

## 🚀 Requisitos e Instalación
1. **Python 3.10+**.
2. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Semillas de Datos (Seed):**
   Puebla la base de datos con **24 coches icónicos** y usuarios de prueba:
   ```bash
   python seed_db.py
   ```

## 🏎️ Guía de Uso
1. **Arrancar Servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```
2. **Documentación Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
3. **Endpoints principales**:
   - `GET /api/v1/cars/`: Ver catálogo.
   - `POST /api/v1/favorites/`: Añadir favorito.
   - `GET /api/v1/favorites/`: Listar favoritos.
   - `PATCH /api/v1/favorites/{car_id}`: Actualizar favorito (rol de usuario).

## 🧪 Testing
El proyecto cuenta con una robusta suite de **33 tests** dividida estratégicamente:

1. **Pruebas Unitarias de Caja Blanca (Aislamiento Total)**:
   Aíslan por completo la capa de aplicación usando Mocks (`unittest.mock`), garantizando un exhaustivo control en las rutas lógicas de:
   - `auth_service` (JWT, Verificaciones de roles estrictas)
   - `car_service` (CRUD)
   - `favorite_service` (Control de duplicados, RBAC)
   - `car_image_service` (Validación de archivos sin manipular el filesystem)
   
   ```bash
   pytest tests/test_unit_*.py
   ```

2. **Pruebas de Integración (API y DB)**:
   Valida el correcto funcionamiento de los endpoints, middlewares y la integridad persistente en la Base de Datos SQLite.
   
   ```bash
   pytest tests/
   ```

## 🔒 Usuarios de Prueba
- **Superadmin**: `admin` / `admin123`
- **User**: `user` / `user123`

---
*Diseñado con ❤️ siguiendo Clean Code, SOLID y Arquitectura Hexagonal.*
