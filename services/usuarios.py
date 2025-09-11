from models.usuarios import Usuarios as UsuariosModel
from schemas.usuarios import Usuarios
from fastapi import HTTPException
from datetime import date


class UsuariosService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_usuarios(self):
        result = self.db.query(UsuariosModel).all()
        return result

    def get_usuario_id(self, id):
        result = self.db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        return result

    def create_usuarios(self, Usuario: Usuarios):
        hoy = date.today()
        fecha_alta = Usuario.fecha_alta

        if fecha_alta is None:
            raise ValueError("fecha_alta no puede ser nula")

        if fecha_alta > hoy:
            raise HTTPException(status_code=404, detail="La fecha de alta no puede ser posterior a hoy")
        new_usuario = UsuariosModel(**Usuario.model_dump(exclude={"id"}))
        self.db.add(new_usuario)
        self.db.commit()
        return
    
    def update_usuarios(self, id: int, data: Usuarios):
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        usuario.nombre_completo = data.nombre_completo
        usuario.email = data.email
        usuario.telefono = data.telefono
        usuario.observaciones = data.observaciones
        usuario.password = data.password        
        self.db.commit()
        return
#USUARIOS: id, nombre, email, telefono, observaciones, fecha_alta

    def delete_usuarios(self, id: int):
       self.db.query(UsuariosModel).filter(UsuariosModel.id == id).delete()
       self.db.commit()
       return
