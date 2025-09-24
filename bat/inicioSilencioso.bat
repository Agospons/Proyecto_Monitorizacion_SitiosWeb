@echo off
chcp 65001 >nul
title Servicio Monitoreo - Segundo Plano

echo ========================================
echo    INICIANDO SERVIDOR EN SEGUNDO PLANO
echo ========================================
echo.

cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"

echo 🔄 Deteniendo procesos anteriores...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1
timeout /t 2 >nul

echo ✅ Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Instalando dependencias...
pip install fastapi uvicorn sqlalchemy requests python-jose passlib python-multipart >nul 2>&1

echo.
echo 🚀 INICIANDO SERVIDOR EN SEGUNDO PLANO...
echo 📍 URL: http://127.0.0.1:8000
echo.

start "ServidorMonitoreo" /min cmd /k "uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo ⏳ Esperando que el servidor inicie (10 segundos)...
timeout /t 10 >nul

echo 🔍 Verificando estado del servidor...
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:8000/docs >nul 2>&1
if not errorlevel 1 (
    echo ✅ Servidor respondiendo correctamente
    echo 🌐 Abriendo documentación de la API...
    timeout /t 2 >nul
    start http://127.0.0.1:8000/docs
    echo.
    echo 💡 IMPORTANTE: La ruta /dashboard no existe
    echo 📊 Usa /dashboard/admin para el dashboard (requiere login)
    echo 📚 Se abrió la documentación en /docs
) else (
    echo ⚠️  El servidor inició pero puede tener problemas
    echo 📋 Abriendo documentación para diagnóstico...
    start http://127.0.0.1:8000/docs
)

echo.
echo ✅ Proceso de inicio completado
echo.
pause