@echo off
chcp 65001 >nul
title Diagnóstico Real del Sistema

echo ========================================
echo    DIAGNÓSTICO REAL - ESTADO ACTUAL
echo ========================================
echo.

echo 🔍 Verificando servidor activo...
tasklist | findstr /i "uvicorn.exe" >nul
if errorlevel 1 (
    echo ❌ Servidor NO está ejecutándose
    echo 💡 Ejecuta la opción 1 del gestor primero
    goto error
)

echo ✅ Servidor activo - Probando rutas...
echo.

curl -s -o response_dashboard.txt -w "Código HTTP de /dashboard: %%{http_code}\n" http://127.0.0.1:8000/dashboard
curl -s -o response_admin.txt -w "Código HTTP de /dashboard/admin: %%{http_code}\n" http://127.0.0.1:8000/dashboard/admin
curl -s -o response_docs.txt -w "Código HTTP de /docs: %%{http_code}\n" http://127.0.0.1:8000/docs

echo.
type response_dashboard.txt
type response_admin.txt
type response_docs.txt

del response_dashboard.txt response_admin.txt response_docs.txt

echo.
echo 📋 INTERPRETACIÓN DE CÓDIGOS HTTP:
echo • 200: ✅ Éxito
echo • 404: ❌ No encontrado (la ruta no existe)
echo • 401: 🔐 No autorizado (requiere login)
echo • 403: ⚠️ Prohibido (sin permisos)

:error
echo.
pause