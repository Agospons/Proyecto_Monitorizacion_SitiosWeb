@echo off
chcp 65001 >nul

echo ========================================
echo    DETENIENDO SERVIDOR
echo ========================================
echo.

echo 🔄 Buscando procesos activos...
tasklist | findstr /i "uvicorn.exe" >nul
if errorlevel 1 (
    echo ℹ️  No hay procesos de uvicorn ejecutándose
) else (
    echo ⚠️  Deteniendo servidor...
    taskkill /f /im uvicorn.exe >nul 2>&1
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 >nul
    echo ✅ Servidor detenido
)

echo.
echo Verificando estado...
tasklist | findstr /i "uvicorn.exe" >nul
if errorlevel 1 (
    echo ✅ Confirmado: Servidor DETENIDO
) else (
    echo ❌ No se pudo detener completamente
    echo Ejecuta 'detener-forzado.bat' si es necesario
)

echo.
pause