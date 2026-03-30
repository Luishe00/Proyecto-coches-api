@echo off
setlocal

set "ROOT=%~dp0"

echo [CarHub] Iniciando backend en http://127.0.0.1:8000 ...
start "CarHub Backend" powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%ROOT%backend'; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [CarHub] Iniciando frontend en http://127.0.0.1:5500 ...
start "CarHub Frontend" powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%ROOT%frontend'; python -m http.server 5500 --bind 127.0.0.1"

timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5500"

echo.
echo [CarHub] Servidores lanzados. Cierra las dos ventanas para detenerlos.
echo.
endlocal
