# 🏎️ Car Catalog API - Arquitectura Hexagonal (100%)

Esta es una API REST profesional para un catálogo de coches de lujo, diseñada bajo los principios de **Arquitectura Hexagonal (Puertos y Adaptadores)**. Ofrece un sistema de roles (RBAC), gestión de favoritos con personalización de color y un núcleo de negocio 100% desacoplado.

## 🌟 Características Destacadas

- **Doble Capa de Color**: 
  - **Color de Fábrica**: Cada coche del catálogo incluye su color original icónico (ej. Ferrari Rosso Corsa).
  - **Personalización Privada**: Los usuarios registrados pueden elegir y actualizar su propio color en su lista de favoritos.
- **Arquitectura Hexagonal Pura**: Separación estricta entre Dominio, Aplicación e Infraestructura.
- **RBAC (Role-Based Access Control)**: Diferenciación clara entre `superadmin` y `user`.
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
3. **Endpoints de Color**:
   - `GET /api/v1/cars/`: Ver catálogo con `color_fabrica`.
   - `POST /api/v1/favorites/`: Añadir favorito con color opcional.
   - `PATCH /api/v1/favorites/{car_id}/color`: Personalizar color (Solo registrados).

## 🧪 Testing

El proyecto cuenta con una robusta suite de **82 tests** (82 passed) con una cobertura total del **93%**, dividida estratégicamente:

1. **Pruebas Unitarias de Caja Blanca y Caja Negra (Aislamiento Total)**:
   - **Técnicas**: Particiones de Equivalencia, Valores Límite, Tablas de Decisión y Cobertura de Sentencia/Decisión.
   - **Alcance**: Validación exhaustiva de la lógica de negocio en `auth_service`, `car_service`, `favorite_service` y esquemas Pydantic.
   - **Aislamiento**: Uso intensivo de Mocks (`unittest.mock`) para garantizar que la lógica es independiente de la base de datos.
   
   ```bash
   # Dentro de la carpeta /backend
   pytest tests/test_unit_*.py
   ```

2. **Pruebas de Integración Reales (Real DB)**:
   - **Tecnología**: Uso de `db_session` con base de datos SQLite en memoria (`test.db`).
   - **Objetivo**: Validar el filtrado dinámico de coches, la persistencia real de usuarios y el funcionamiento de la paginación (`skip/limit`) sin mocks.
   
   ```bash
   # Ejecuta todos los tests con reporte de cobertura
   pip install pytest-cov
   python -m pytest --cov=app tests/
   ```

## 📊 Estadísticas de Cobertura Final
- **Total de Tests**: 82 (Passed)
- **Cobertura Total**: 93%
- **Servicios de Negocio**: 98% - 100% de cobertura individual.

## 🔒 Usuarios de Prueba
- **Superadmin**: `admin` / `admin123`
- **User**: `user` / `user123`

---
*Diseñado con ❤️ siguiendo Clean Code, SOLID y Arquitectura Hexagonal.*
