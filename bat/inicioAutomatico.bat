@echo off
chcp 65001 >nul

echo ========================================
echo    INSTALAR INICIO AUTOMÁTICO
echo ========================================
echo.

set "RUTA_SCRIPT=%~dp0iniciar-silencioso.bat"

echo 🔄 Configurando inicio automático...
powershell -Command "
$WshShell = New-Object -ComObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\MonitoreoSitios.lnk');
$Shortcut.TargetPath = '%RUTA_SCRIPT%';
$Shortcut.WorkingDirectory = '%~dp0';
$Shortcut.WindowStyle = 7;
$Shortcut.Description = 'Servicio de Monitoreo de Sitios Web';
$Shortcut.Save();
"

echo ✅ Configurado para inicio automático
echo.
echo El servidor se iniciará automáticamente cuando:
echo • Enciendas la computadora
echo • Inicies sesión en Windows
echo.
echo Ubicación del acceso directo:
echo %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MonitoreoSitios.lnk
echo.
pause