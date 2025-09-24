from fastapi import APIRouter
from fastapi import Depends, Path, Query,  HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_database_session
from models.usuarios import Usuarios as UsuarioModel
from fastapi.encoders import jsonable_encoder
from security.jwt_bearer import JWTBearer
from services.usuarios import UsuariosService
from passlib.context import CryptContext
from security.jwt_manager import create_token
from schemas.usuarios import User, UsuarioBase, Usuarios, UsuariosOut

usuarios_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(users:dict, email: str, password: str)->UsuariosOut:
    user = get_user(users, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    user = UsuariosOut.from_orm(user)
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(users:list, email: str):
    for item in users:
        if item.email == email:
            return item
        
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  

@usuarios_router.post('/login', tags=['Autenticacion'])
def login(user: User, db=Depends(get_database_session)):
    
    usuariosDb:UsuarioModel = UsuariosService(db).get_usuarios()

    usuario= authenticate_user(usuariosDb, user.email, user.password)
    if not usuario:
       return JSONResponse(status_code=401, content={'accesoOk': False,'token':''})  
    else:
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={'accesoOk': True,'token':token, 'usuario': jsonable_encoder(usuario) })


@usuarios_router.get("/usuarios", tags=["Usuarios"], status_code=status.HTTP_200_OK,response_model=List[UsuariosOut], dependencies=[Depends(JWTBearer())])
def get_usuarios(db=Depends(get_database_session)):
    result = UsuariosService(db).get_usuarios()
    return result


@usuarios_router.get('/usuarios/{id}', tags=['Usuarios'], response_model=UsuariosOut,
                     status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_usuarioxId(id: int , db=Depends(get_database_session)):
    result = UsuariosService(db).get_usuario_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return result

@usuarios_router.post('/usuarios', tags=['Usuarios'], response_model=dict, status_code=201)
def create_usuarios(usuario: Usuarios, db=Depends(get_database_session)) -> dict:
    usuario.password = get_password_hash(usuario.password)
    #db = Session()
    UsuariosService(db).create_usuarios(usuario)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el usuario"})


@usuarios_router.put('/usuarios/{id}', tags=['Usuarios'], response_model=dict, status_code=200)
def update_usuarios(id: int, usuarios: Usuarios, db = Depends(get_database_session))-> dict:
    result = UsuariosService(db).get_usuario_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No se encontro el usuario"})
    usuarios.password = get_password_hash(usuarios.password)
    UsuariosService(db).update_usuarios(id, usuarios)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el usuario"})


@usuarios_router.delete('/usuarios/{id}', tags=['Usuarios'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_usuarios(id: int, db = Depends(get_database_session))-> dict:
    result: UsuarioModel = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontro el usuario"})
    UsuariosService(db).delete_usuarios(id)
    return JSONResponse(status_code=200, content={"message": "Se elimino el usuario"})