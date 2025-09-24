@echo off
chcp 65001 >nul
title Solucionar Error de Conexión

echo ========================================
echo    SOLUCIONANDO ERROR DE CONEXIÓN
echo ========================================
echo.

echo 🔍 Diagnóstico del sistema...
echo.

echo 1. Verificando procesos Python...
tasklist /fi "imagename eq python.exe" /fo table

echo.
echo 2. Verificando uso del puerto 8000...
netstat -ano | findstr :8000

echo.
echo 3. Deteniendo procesos conflictivos...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1

timeout /t 2 >nul

echo.
echo 4. Verificando entorno virtual...
cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"

if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: No se encuentra el entorno virtual
    echo Creando entorno virtual...
    python -m venv venv
)

echo.
echo 5. Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo 6. Instalando dependencias...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo ⚠️  No hay requirements.txt, instalando dependencias básicas...
    pip install fastapi uvicorn sqlalchemy requests
)

echo.
echo 🚀 INICIANDO SERVIDOR...
echo 📍 URL: http://127.0.0.1:8000
echo 🌐 Dashboard: http://127.0.0.1:8000/dashboard
echo.
echo ⏹️  Presiona Ctrl+C para detener
echo ========================================
echo.

uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause