from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, Path, Query,  HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_database_session
from fastapi.encoders import jsonable_encoder
from security.jwt_bearer import JWTBearer
from services.sitios import SitiosService
from passlib.context import CryptContext
from security.jwt_manager import create_token
from schemas.sitios import Sitios, sitiosOut
from models.sitios import Sitios as SitiosModel
from models.log_chequeo import Log_chequeo as LogoModels
from schemas.log_chequeo import Log_chequeo, logOut

from datetime import date
hoy = date.today()

sitios_routers = APIRouter()

@sitios_routers.post("/sitios", tags=["Sitios"], response_model=dict, status_code=201)
def crear_sitios(sitios: Sitios, db=Depends(get_database_session)) -> dict:
    SitiosService(db).create_Sitios(sitios)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el sitio web"})


@sitios_routers.get("/sitios", tags=["Sitios"], response_model=List[sitiosOut], status_code=status.HTTP_200_OK)
def get_sitios(db = Depends(get_database_session)):
    resultado = SitiosService(db).get_sitios()
    return resultado


@sitios_routers.get("/sitios/{id}", tags=["Sitios"], response_model=sitiosOut, status_code=status.HTTP_200_OK)
def get_sitios_id(id : int, db = Depends(get_database_session)):
    resultado = SitiosService(db).get_sitios_id(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sitio no encontrado")
    return resultado


@sitios_routers.put("/sitios/{id}", tags=["Sitios"], response_model=dict, status_code=201)
def uptdate_sitio(id: int, sitios: Sitios, db=Depends(get_database_session))-> dict:
    resultado = SitiosService(db).get_sitios_id(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sitio web no encontrado")
    SitiosService(db).update_Sitios(id, sitios)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el sitios web"})



@sitios_routers.delete("/sitios/{id}", tags=["Sitios"], response_model=dict, status_code=201)
def eliminar_sitio(id: int, db=Depends(get_database_session)):
    result: SitiosModel = db.query(SitiosModel).filter(SitiosModel.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sitio web no encontrado")
    SitiosService(db).delete_sitios(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el sitio web"})



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

@sitios_routers.get("/sitios/{id}", tags=["Sitios"], response_model=dict, status_code=200)
def verificar_sitio(id: int, db=Depends(get_database_session)):
    servicio = SitiosService(db)
    resultado = servicio.chequear_sitio(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")

    return resultado