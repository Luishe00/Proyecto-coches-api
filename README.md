# Catálogo de Coches - API Backend

Esta es una API REST completa para un catálogo de coches, con soporte de roles (RBAC) y filtrado avanzado. Construida sobre Python 3.10+ y FastAPI, soportada por MySQL y SQLAlchemy.

## Requisitos Previos
1. **Python 3.10+**.
2. **XAMPP** con el módulo de MySQL activado.

## Instalación y Configuración Básica
1. **Arrancar XAMPP:**
   Inicia la aplicación XAMPP y arranca el módulo "MySQL". Asegúrate de que está corriendo en el puerto `3306`.

2. **Crear base de datos:**
   Ve a phpMyAdmin (`http://localhost/phpmyadmin`) o usa la consola de MySQL para crear la base de datos `car_catalog`:
   ```sql
   CREATE DATABASE car_catalog;
   ```

3. **Instalar Dependencias:**
   Dentro de la carpeta `/backend`, crea un entorno virtual (opcional pero recomendado) y corre:
   ```bash
   pip install -r requirements.txt
   ```

4. **Semillas de Datos (Seed):**
   Para probar la API, puedes poblarla con datos iniciales ejecutando el siguiente comando dentro de la carpeta `/backend`:
   ```bash
   python seed.py
   ```
   *Esto limpiará las tablas existentes y añadirá 2 usuarios (admin y normal) y 24 coches.*

## Ejecución del Servidor
Para correr el servidor de desarrollo, estando situado en la carpeta `/backend`:
```bash
uvicorn app.main:app --reload
```
Una web auto-documentada usando Swagger estará disponible en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Ejecución de Tests
Para asegurar la fiabilidad de la API, se han definido tests de integración. Para ejecutarlos usa:
```bash
pytest tests/
```

## Estructura de Roles Pordefecto
* **Rol Superadmin:**
  - Login: `admin` / Password: `admin123`
  - Permisos: Leer, Crear, Actualizar y Eliminar coches.

* **Rol User:**
  - Login: `user` / Password: `user123`
  - Permisos: Solo permisos de lectura (Leer listado, buscar, filtrar).
