@echo off
chcp 65001 >nul

echo ========================================
echo    ESTADO DEL SERVIDOR
echo ========================================
echo.

tasklist /fi "imagename eq python.exe" /fo table | findstr /i "uvicorn" >nul
if errorlevel 1 (
    echo ❌ Servidor NO está ejecutándose
    echo.
    echo Para iniciar: iniciar-silencioso.bat
) else (
    echo ✅ Servidor ACTIVO
    echo 📍 http://127.0.0.1:8000
    echo.
    
    :: Probar conexión
    curl -s -o nul -w "%%{http_code}" http://127.0.0.1:8000/ > status.txt 2>&1
    set /p STATUS=<status.txt
    del status.txt
    
    if "%STATUS%"=="200" (
        echo 🌐 Conexión: ✅ EXITOSA
    ) else (
        echo 🌐 Conexión: ⚠️  PROBLEMAS (Código: %STATUS%)
    )
)

echo.
echo Procesos activos:
tasklist /fi "imagename eq python.exe" /fo table

echo.
pause
