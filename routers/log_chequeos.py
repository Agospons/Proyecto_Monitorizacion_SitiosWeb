from fastapi import APIRouter
from fastapi import Depends, Path, Query,  HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_database_session
from fastapi.encoders import jsonable_encoder
from security.jwt_bearer import JWTBearer
from passlib.context import CryptContext
from security.jwt_manager import create_token
from models.sitios import Sitios as SitiosModel
from schemas.log_chequeo import Log_chequeo, logOut
from models.log_chequeo import Log_chequeo as LogModel
from services.log_chequeo import LogService


from datetime import date
hoy = date.today()

logeos_routers = APIRouter()


@logeos_routers.post("/logeos", tags=["Logs"], response_model=dict, status_code=201)
def crear_logs(log:Log_chequeo, db=Depends(get_database_session)) -> dict:
    LogService(db).crear_logeo(log)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el log"})


@logeos_routers.get("/logeos", tags=["Logs"], response_model=List[logOut], status_code=status.HTTP_200_OK)
def get_log(db=Depends(get_database_session)):
    result = LogService(db).get_logeo()
    return result


@logeos_routers.get("/logeos/{id}", tags=["Logs"], response_model=logOut, status_code=status.HTTP_200_OK)
def get_log_id(id:int, db=Depends(get_database_session)):
    resultado = LogService(db).get_log_id(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log no encontrado")
    return resultado


@logeos_routers.put("/logeos/{id}", tags=["Logs"], response_model=dict, status_code=201)
def actualizar_log(id: int, log: Log_chequeo,  db=Depends(get_database_session)):
    resultado = LogService(db).get_log_id(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log no encontrado")
    LogService(db).update_logeo(id, log)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el log"})


@logeos_routers.delete("/logeos/{id}", tags=["Logs"], response_model=dict, status_code=201)
def eliminar_log(id: int, db=Depends(get_database_session)):
    resultado: LogModel = db.query(LogModel).filter(LogModel.id == id).first()
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log no encontrado")
    LogService(db).delete_logeo(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el log"})
