@echo off
chcp 65001 >nul
title Gestor de Servicio de Monitoreo

:menu
cls
echo ========================================
echo    GESTOR DEL SERVICIO DE MONITOREO
echo ========================================
echo.
echo 1. 🔄 Iniciar servidor (CON LOGS)
echo 2. ⏹️  Detener servidor
echo 3. 📊 Ver estado
echo 4. 🌐 Abrir DOCUMENTACIÓN API
echo 5. 📈 Abrir INDEX INICIO SECION
echo 6. 🔍 Ver rutas disponibles
echo 7. ⚙️  Instalar inicio automático
echo 8. ❌ Salir
echo.

set /p opcion="Selecciona una opción (1-8): "

if "%opcion%"=="1" goto iniciar
if "%opcion%"=="2" goto detener
if "%opcion%"=="3" goto estado
if "%opcion%"=="4" goto docs
if "%opcion%"=="5" goto dashboard-admin
if "%opcion%"=="6" goto rutas
if "%opcion%"=="7" goto inicio-auto
if "%opcion%"=="8" goto exit

echo Opción no válida
timeout /t 2 >nul
goto menu

:iniciar
echo 🚀 INICIANDO SERVIDOR CON LOGS VISIBLES...
echo ⚠️  Esta ventana mostrará los logs del servidor
echo ⏹️  Presiona Ctrl+C para detener
echo ========================================
echo.
cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"
call venv\Scripts\activate.bat
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
goto menu

:detener
call detener.bat
goto menu

:estado
call estado.bat
goto menu

:docs
echo 📚 Abriendo Documentación de la API...
start http://127.0.0.1:8000/docs
goto menu

:dashboard-admin
echo ⚠️  ABRIENDO INICIO DE SECION ...
echo 📋 Nota: Esta ruta requiere autenticación JWT
echo 🔐 Si no estás logueado, te redirigirá a login
start http://127.0.0.1:5501/html/index.html
goto menu

:rutas
echo 🔍 Listando rutas disponibles...
cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"
call venv\Scripts\activate.bat

python -c "
try:
    from main import app
    print('📋 RUTAS DISPONIBLES EN LA APLICACIÓN:')
    print('=' * 60)
    
    for route in app.routes:
        if hasattr(route, 'path'):
            path = route.path
            methods = ', '.join(route.methods) if hasattr(route, 'methods') else 'GET'
            print(f'{path} ({methods})')
    
    print('')
    print('💡 INFORMACIÓN IMPORTANTE:')
    print('• La ruta /dashboard NO existe')
    print('• Usa /dashboard/admin (requiere autenticación)')
    print('• Usa /docs para la documentación interactiva')
    
except Exception as e:
    print(f'❌ Error: {e}')
"
echo.
pause
goto menu

:inicio-auto
if exist "inicioAutomatico.bat" (
    call inicioAutomatico.bat
) else (
    echo ❌ Archivo inicioAutomatico.bat no encontrado
)
goto menu

:exit
echo.
echo ¡Hasta pronto!
timeout /t 2 >nul