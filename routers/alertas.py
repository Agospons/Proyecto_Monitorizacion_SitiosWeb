from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_database_session
from services.alertas import AlertasServices
from schemas.alertas import alertasOut, Alertas

from datetime import date
hoy = date.today()

alertas_routers = APIRouter()

@alertas_routers.post("/alertas", tags=["Alertas"], response_model=dict, status_code=201)
def crear_alertas(alerta: Alertas, db=Depends(get_database_session)) -> dict:
    AlertasServices(db).crear_alerta(alerta)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la alerta"})



@alertas_routers.put("/alertas", tags=["Alertas"], response_model=dict, status_code=201)
def update_alerta(id: int, alerta: Alertas, db=Depends(get_database_session)) -> dict:
    result = AlertasServices(db).get_alerta_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrado")
    AlertasServices(db).actualizar_alertas(id, alerta)
    raise HTTPException(status_code=201, detail="Alerta actualizada")



# @sitios_routers.delete("/sitios/{id}", tags=["Sitios"], response_model=dict, status_code=201)
# def eliminar_sitio(id: int, db=Depends(get_database_session)):
#     result: SitiosModel = db.query(SitiosModel).filter(SitiosModel.id == id).first()
#     if not result:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sitio web no encontrado")
#     SitiosService(db).delete_sitios(id)
#     return JSONResponse(status_code=200, content={"message": "Se ha eliminado el sitio web"})

