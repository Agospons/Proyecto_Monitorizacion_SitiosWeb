from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_database_session
from services.alertas import AlertasServices
from schemas.alertas import alertasOut, Alertas
from models.alertas import Alertas as AlertasModels

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

@alertas_routers.delete("/alertas/{id}", tags=["Alertas"], response_model=dict, status_code=201)
def eliminar_alertas(id: int, db=Depends(get_database_session)):
    result: AlertasModels = db.query(AlertasModels).filter(AlertasModels.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrado")
    AlertasServices(db).delete_alertas(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la alerta"})
