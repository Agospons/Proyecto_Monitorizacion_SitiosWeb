from fastapi import APIRouter
from typing import List
from security.jwt_bearer import JWTBearer
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_database_session
from services.alertas import AlertasServices
from schemas.alertas import Alertas, alertasOut
from models.alertas import Alertas as AlertasModels
from datetime import date

alertas_routers = APIRouter()


@alertas_routers.post("/alertaa/auto", tags=["Alertas"], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def crear_alertas_automaticas(db=Depends(get_database_session)) -> dict:
    AlertasServices(db).crear_alerta_automatica()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la alerta"})



@alertas_routers.post("/alertas", tags=["Alertas"], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def crear_alertas(alerta: Alertas, db=Depends(get_database_session)) -> dict:
    AlertasServices(db).crear_alerta(alerta)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la alerta"})



@alertas_routers.get("/alertas", tags=["Alertas"], response_model=List[alertasOut], dependencies=[Depends(JWTBearer())])
def obtener_alertas(db=Depends(get_database_session)):
    try:
        alertas = AlertasServices(db).get_alertas()
        if not alertas:
            return []
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alertas: {str(e)}")



@alertas_routers.get("/alertas/hoy", tags=["Alertas"], response_model=List[alertasOut], dependencies=[Depends(JWTBearer())])
def obtener_alertas_hoy(db=Depends(get_database_session)):
    try:
        alertas = AlertasServices(db).get_alertas_hoy()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alertas de hoy: {str(e)}")


@alertas_routers.put("/alertas/{id}", tags=["Alertas"], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_alerta(id: int, alerta: Alertas, db=Depends(get_database_session)) -> dict:
    result = AlertasServices(db).get_alerta_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")
    AlertasServices(db).actualizar_alertas(id, alerta)
    return JSONResponse(status_code=200, content={"message": "Alerta actualizada"})


@alertas_routers.delete("/alertas/{id}", tags=["Alertas"], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def eliminar_alertas(id: int, db=Depends(get_database_session)):
    result: AlertasModels = db.query(AlertasModels).filter(AlertasModels.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")
    AlertasServices(db).delete_alertas(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la alerta"})

