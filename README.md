# CarHub Local Starter

Repositorio con backend FastAPI + frontend SPA en JavaScript.

## Opcion 1 - Arranque con 1 clic (Windows)

1. Haz doble clic en `start-local.bat`.
2. Se abriran dos ventanas:
   - Backend: `http://127.0.0.1:8000`
   - Frontend: `http://127.0.0.1:5500`
3. El navegador se abrira automaticamente en el frontend.

## Opcion 2 - Arranque manual (cualquier sistema)

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

### 3) Abrir aplicacion

Abre en el navegador:

- `http://127.0.0.1:5500`

## Nota importante

Abrir `index.html` con doble clic usa `file://` y no es un servidor HTTP.
Para que funcione correctamente la SPA, siempre hay que levantar un servidor local (opcion 1 u opcion 2).

## Documentacion adicional

- Backend completo: `backend/README.md`
- Frontend visual: `frontend/README.md`
