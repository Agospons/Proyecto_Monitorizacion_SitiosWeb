@echo off
chcp 65001 >nul
title Arreglar Error de Importación Circular

echo ========================================
echo    ARREGLANDO ERROR DE IMPORTACIÓN
echo ========================================
echo.

echo 🔄 Deteniendo servidor...
call detener.bat

echo.
echo 🔍 Buscando error en dashboard.py...
cd /d "C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS"

if exist "routers\dashboard.py" (
    echo ✅ dashboard.py encontrado
    echo 📝 Verificando contenido...
    
    findstr /i "from main import app" "routers\dashboard.py" >nul
    if errorlevel 1 (
        echo ✅ No se encontró la línea problemática
    ) else (
        echo ❌ Se encontró la línea problemática
        echo 🔧 Creando backup y arreglando...
        copy "routers\dashboard.py" "routers\dashboard_backup.py"
        
        powershell -Command "
        $content = Get-Content 'routers\dashboard.py' -Encoding UTF8
        $newContent = @()
        foreach ($line in $content) {
            if (-not $line.Contains('from main import app')) {
                $newContent += $line
            }
        }
        Set-Content 'routers\dashboard.py' $newContent -Encoding UTF8
        "
        echo ✅ Línea problemática eliminada
    )
) else (
    echo ❌ dashboard.py no encontrado
)

echo.
echo 🚀 Probando importación...
call venv\Scripts\activate.bat

python -c "
try:
    from main import app
    print('✅ main.py se importa correctamente')
    print('✅ Error de importación circular solucionado')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo.
echo 💡 Ahora ejecuta la opción 1 de gestionar.bat
echo.
pause