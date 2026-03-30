# CarHub Frontend

<div align="center">

## Interfaz SPA para catalogo premium de coches

Frontend en JavaScript modular que consume la API de CarHub y muestra catalogo, autenticacion y favoritos.

| Entorno | URL |
|---|---|
| Frontend | `http://127.0.0.1:5500` |
| API | `http://127.0.0.1:8000/api/v1` |
| Swagger | `http://127.0.0.1:8000/docs` |

</div>

---

## Vista general

- SPA renderizada desde `js/app.js`
- Cliente HTTP centralizado en `js/api.js`
- Modulos separados por responsabilidad (`auth.js`, `cars.js`, `utils.js`)
- Estilos y animaciones en `assets/css/`

## Estructura

```text
frontend/
  index.html
  assets/
    css/
      style.css
      animations.css
  js/
    api.js
    app.js
    auth.js
    cars.js
    utils.js
```

## Como arrancarlo rapido

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Luego abre:

- `http://127.0.0.1:5500`

## Flujo funcional

1. El navegador carga `index.html`.
2. `js/app.js` construye la UI dinamicamente.
3. Las acciones del usuario llaman a `js/api.js`.
4. `api.js` habla con FastAPI en `http://localhost:8000/api/v1`.
5. El token JWT se guarda y reutiliza desde `localStorage`.

## Recomendaciones de desarrollo

- No abrir `index.html` por doble clic (`file://`), usar siempre HTTP local.
- Si cambias el puerto de la API, actualiza `API_BASE` en `js/api.js`.
- Mantener la separacion por modulos para evitar logica mezclada de UI/API.

## Checklist rapido

- [ ] Backend arriba en puerto 8000
- [ ] Frontend servido en puerto 5500
- [ ] Login devuelve token
- [ ] Catalogo carga sin errores en consola

---

Disenado para demos locales rapidas, presentaciones y practica de arquitectura por capas.
