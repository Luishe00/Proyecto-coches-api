# CarHub Local Starter

Repositorio con backend FastAPI + frontend SPA en JavaScript.

## Opción 1 - Arranque con 1 clic (Windows)

1. Haz doble clic en `start-local.bat`.
2. Se abrirán dos ventanas:
   - Backend: `http://127.0.0.1:8000`
   - Frontend: `http://127.0.0.1:5500`
3. El navegador se abrirá automáticamente en el frontend.

## Opción 2 - Arranque manual (cualquier sistema)

### 1) Backend

```bash
cd backend
pip install -r requirements.txt
python seed_db.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2) Frontend (otra terminal)

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

### 3) Abrir aplicación

Abre en el navegador:

- `http://127.0.0.1:5500`

## Nota importante

Abrir `index.html` con doble clic usa `file://` y no es un servidor HTTP.
Para que funcione correctamente la SPA, siempre hay que levantar un servidor local (opción 1 u opción 2).

## Documentación adicional

- Backend completo: `backend/README.md`
- Frontend visual: `frontend/README.md`
