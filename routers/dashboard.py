from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from database import get_database_session
from security.jwt_bearer import JWTBearer
from services.dashboard import DashboardService
from schemas.dashboard import DashboardStats, Dash
from schemas.log_chequeo import logOut

dashboard_router = APIRouter()

@dashboard_router.get(
    "/dashboard/admin",
    tags=["Dashboard"],
    response_model=DashboardStats,
    #dependencies=[Depends(JWTBearer())]
)
def obtener_dashboard_stats(db=Depends(get_database_session)):
    service = DashboardService(db)
    return {
        "sitios_online": service.sitios_online(),
        "sitios_offline": service.sitios_offline(),
        "dominio_vencido": service.sitios_dominio_vencido(),
        "ultimos_usuarios": service.ultimos_usuarios_registrados(),
        "web_no_online": service.web_no_online()
    }


@dashboard_router.get("/dashboard/admin/{id}", tags=["Dashboard"], response_model=Dash)
def sitiosWebHistorial(id: int, db=Depends(get_database_session)):
    logs = DashboardService(db).historial_sitios(id)
    if not logs:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    return {"historial_sitios": logs}