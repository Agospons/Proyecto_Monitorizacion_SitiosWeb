@echo off
chcp 65001 >nul

echo ========================================
echo    VERIFICACIÓN ESPECÍFICA - DASHBOARD
echo ========================================
echo.

cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"
call venv\Scripts\activate.bat

python verificar-dashboard.py

echo.
echo 🌐 Probando conexiones...
echo.
curl -s -o nul -w "Dashboard: %%{http_code}\n" http://127.0.0.1:8000/dashboard
curl -s -o nul -w "Docs:      %%{http_code}\n" http://127.0.0.1:8000/docs
curl -s -o nul -w "Home:      %%{http_code}\n" http://127.0.0.1:8000/

echo.
pause