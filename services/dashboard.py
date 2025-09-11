from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from models.usuarios import Usuarios as UsuariosModel
from models.alertas import Alertas as AlertasModel
from models.sitios import Sitios as SitiosModel

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


        # self.db.query(UsuariosModel)
        # .order_by(UsuariosModel.fecha_alta.desc())
        # .limit(limite)
        # .all()
    
    
    # def top_usuarios_por_reservas(self, limite: int = 5):
    #     return (
    #         self.db.query(
    #             UsuariosModel.id,
    #             UsuariosModel.nombre,
    #             UsuariosModel.apellido,
    #             func.count(ReservasModel.id).label("total_reservas")
    #         )
    #         .join(ReservasModel)
    #         .group_by(UsuariosModel.id)
    #         .order_by(func.count(ReservasModel.id).desc())
    #         .limit(limite)
    #         .all()
    #     )