from fastapi import APIRouter
from fastapi import Depends
from database import get_database_session
from security.jwt_bearer import JWTBearer
from services.dashboard import DashboardService
from schemas.dashboard import DashboardStats

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