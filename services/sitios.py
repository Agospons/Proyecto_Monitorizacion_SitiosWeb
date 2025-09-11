from models.sitios import Sitios as SitiosModel
from schemas.sitios import Sitios
from models.usuarios import Usuarios as UsuariosModel
from fastapi import HTTPException
from fastapi import HTTPException
from datetime import date


class SitiosService():
    def __init__(self, db) -> None:
       self.db = db
    
    def create_Sitios(self, sitios: Sitios):
        hoy = date.today()
        fecha_alta = sitios.fecha_alta

        if fecha_alta is None:
            raise ValueError("fecha_alta no puede ser nula")

        if fecha_alta > hoy:
            raise HTTPException(status_code=404, detail="La fecha de alta no puede ser posterior a hoy")
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == sitios.id_cliente).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        ip = self.db.query(SitiosModel).filter(SitiosModel.ip == sitios.ip).first()
        if ip:
            raise HTTPException(status_code=404, detail="La direccion IP ya esta registrada")
        nuevo_sitio = SitiosModel(**sitios.dict())
        self.db.add(nuevo_sitio)
        self.db.commit()
        return nuevo_sitio

    def get_sitios(self):
        resultado = self.db.query(SitiosModel).all()
        return resultado
    
    def get_sitios_id(self, id:int):
        resultado = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        return resultado
    
    def update_Sitios(self, idd: int, data: Sitios):
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == data.id_cliente).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == idd).first()
        sitio.dominio = data.dominio
        sitio.ip = data.ip
        sitio.servidor = data.servidor
        sitio.id_cliente = data.id_cliente
        sitio.notas = data.notas
        sitio.estado = data.estado
        sitio.ultima_revision = data.ultima_revision
        sitio.vencimiento_dominio = data.vencimiento_dominio
        sitio.estado_dominio = data.estado_dominio
        sitio.fecha_alta = data.fecha_alta
        self.db.commit()
        return 
    
    def delete_sitios(self, id: int):
        self.db.query(SitiosModel).filter(SitiosModel.id == id).delete()
        self.db.commit()
        return 
    