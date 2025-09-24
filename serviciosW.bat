@echo off
echo Instalando servicio de notificaciones de dominios...
echo.

sc create NotificadorDominios binPath= "\"C:\Python39\python.exe\" \"C:\Users\Agostina\PycharmProjects\AAPROYECTO PASANTIAS\notificaciones.py\"" start= auto
@REM carpeta que se cambia al mandar a otra computadora
echo.
echo Servicio instalado correctamente!
echo.
echo Para iniciar el servicio ejecuta: sc start NotificadorDominios
echo Para ver el estado: sc query NotificadorDominios
echo Para detener: sc stop NotificadorDominios
echo Para eliminar: sc delete NotificadorDominios

pause