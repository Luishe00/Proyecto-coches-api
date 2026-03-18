# 🏎️ Car Catalog API - Arquitectura Hexagonal (100%)

Esta es una API REST profesional para un catálogo de coches, diseñada siguiendo los principios de la **Arquitectura Hexagonal (Puertos y Adaptadores)**. Ofrece un sistema robusto de roles (RBAC), gestión de favoritos y un núcleo de negocio totalmente desacoplado de la infraestructura.

## 🏗️ Arquitectura
El proyecto ha sido refactorizado para garantizar un desacoplamiento total:
- **Dominio**: Entidades puras en `app/domain/entities.py`. Zero dependencias.
- **Servicios**: Lógica de negocio agnóstica al framework.
- **Adaptadores**: Implementaciones concretas para FastAPI (Web) y SQLAlchemy (Persistencia).

## 🚀 Requisitos Previos
1. **Python 3.10+**.
2. No se requiere XAMPP ni MySQL (migrado a **SQLite** para máxima portabilidad).

## 🛠️ Instalación y Configuración
1. **Clonar el repositorio** y acceder a la carpeta `/backend`.
2. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar Entorno:**
   Copia `.env.example` a `.env` y ajusta las variables si es necesario.
   ```bash
   cp .env.example .env
   ```
4. **Semillas de Datos (Seed):**
   Para poblar la base de datos con los 24 coches iniciales y usuarios de prueba:
   ```bash
   python seed_db.py
   ```

## 🏎️ Ejecución
Para arrancar el servidor de desarrollo:
```bash
uvicorn app.main:app --reload
```
Accede a la documentación Interactiva (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## 🧪 Testing
El proyecto incluye una suite completa de tests que validan tanto la integración como la lógica de negocio pura:
- **Ejecutar todos los tests:**
  ```bash
  pytest tests/
  ```
- **Tests Unitarios (Mocks):** `tests/test_unit_cars.py`
- **Tests Integración (DB):** `tests/test_cars.py`, `tests/test_auth.py`, `tests/test_favorites.py`.

## 🔒 Roles y Seguridad
* **Superadmin (`admin` / `admin123`)**: Control total sobre el catálogo de coches.
* **User (`user` / `user123`)**: Acceso a lectura y gestión de su propia lista de **Favoritos**.

---
*Diseñado con ❤️ siguiendo Clean Code y Principios SOLID.*
