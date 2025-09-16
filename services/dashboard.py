from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from models.usuarios import Usuarios as UsuariosModel
from models.alertas import Alertas as AlertasModel
from models.sitios import Sitios as SitiosModel
from models.log_chequeo import Log_chequeo as LogModel
from schemas.log_chequeo import Log_chequeo
from fastapi import HTTPException


# Sitios Online
# Sitios Ofline
# Errores
# Problemas

class DashboardService:

    def __init__(self, db):
        self.db = db

    
    def sitios_online(self):
        return self.db.query(SitiosModel).filter(SitiosModel.estado == "online").count()

    def sitios_offline(self):
        return self.db.query(SitiosModel).filter(SitiosModel.estado == "offline").count()

    def sitios_dominio_vencido(self):
        return self.db.query(SitiosModel).filter(SitiosModel.estado_dominio == "vencido").count()
    

    def ultimos_usuarios_registrados(self, limite: int = 5):
        return (
        self.db.query(UsuariosModel)
        .order_by(UsuariosModel.fecha_alta.desc())
        .limit(limite)
        .all()
    )
    
    def web_no_online(self):
        return (
        self.db.query(SitiosModel)
        .filter(SitiosModel.estado == "offline")
        .order_by(SitiosModel.ultima_revision.desc())
        .all()
    )

    def historial_sitios(self, id:int, limite: int = 5):
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")

        result = (
            self.db.query(LogModel)
            .filter(LogModel.id_sitio == id)
            .limit(limite)
            .all()
        )
        return result
    
    
