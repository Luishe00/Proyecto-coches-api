# Arquitectura del Backend: Catálogo de Coches

El proyecto sigue una arquitectura monolítica modular basada en capas (Service/Repository Pattern) construida con FastAPI y SQLAlchemy.

## Flujo de Peticiones
1. **Router (`app/routers/`):** Define los endpoints de la API, recibe los datos del cliente (validados automáticamente usando schemas Pydantic) y delega la ejecución al servicio correspondiente.
2. **Service (`app/services/`):** Contiene la lógica de negocio y las reglas de validación complejas, y ejecuta la manipulación de datos en la base de datos a través de SQLAlchemy.
3. **Database Models (`app/models/`):** Definen la estructura de la tabla en MySQL.
4. **Schemas (`app/schemas/`):** Definen la estructura de los datos esperados en las Requests y Responses. Valida los rangos (por ejemplo, año entre 1886 y 2027) antes de que el controlador empiece a procesar la solicitud.

## Flujo de Seguridad (JWT y RBAC)
1. **Registro/Login:** El usuario hace POST a `/api/v1/auth/login`. El servicio verifica las credenciales y devuelve un token JWT (`app/core/security.py`).
2. **Autorización:** Para acceder a endpoints protegidos, el cliente envía un Header `Authorization: Bearer <token>`.
3. **RBAC (Role Based Access Control):** 
   - La dependencia `get_current_active_user` en `auth_service.py` lee el JWT, busca el usuario y lo inyecta al router.
   - La dependencia `get_current_superadmin_user` hace un paso adicional: comprueba si el `role` del usuario es `RoleEnum.superadmin`. Si no es así, devuelve un error 403 Forbidden.
   - Operaciones de Solo Lectura (`GET /cars` o `GET /cars/{id}`) son públicas o limitadas al token genérico.
   - Operaciones Transaccionales (`POST`, `PUT`, `DELETE` sobre `/cars`) requieren el token firmado por un `superadmin`.

## Componentes Clave
- **FastAPI:** Framework web rápido y moderno.
- **SQLAlchemy:** ORM que traduce objetos Python a filas y queries en MySQL.
- **Pydantic:** Librería de parseo rápido y validación de tipos utilizada exhaustivamente en schemas.
- **Passlib/Bcrypt:** Para no guardar las contraseñas en texto plano.
- **Pytest/Httpx:** Testing unitario y de integración asíncrono.
