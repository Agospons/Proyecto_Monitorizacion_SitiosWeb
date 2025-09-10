from models.sitios import Sitios as SitiosModel
from models.alertas import Alertas as AlertasModel
from schemas.alertas import Alertas 
from fastapi import HTTPException


class AlertasServices():
    def __init__(self, db) -> None:
       self.db = db
    
    def crear_alerta(self, alerta:Alertas):
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == alerta.id_sitio).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")

        nueva_alerta = AlertasModel(**alerta.dict())
        self.db.add(nueva_alerta)
        self.db.commit()
        return nueva_alerta
    
    # def crear_logeo(self, logeo: Log_chequeo):
    #     sitio = self.db.query(SitiosModel).filter(SitiosModel.id == logeo.id_sitio).first()
    #     if not sitio:
    #         raise HTTPException(status_code=404, detail="Sitio web no encontrado")
    #     nuevolog = LogModel(**logeo.dict())
    #     self.db.add(nuevolog)
    #     self.db.commit()
    #     return nuevolog

    
    def get_alertas(self):
        alerta = self.db.query(AlertasModel).all()
        return alerta

    def get_alerta_id(self, id:int):
        resultado = self.db.query(AlertasModel).filter(AlertasModel.id == id).first()
        return resultado
    
    def actualizar_alertas(self, id:int, alerta:Alertas):
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == alerta.id_sitio).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")
        
        alert = self.db.query(AlertasModel).filter(AlertasModel.id == id).first()
        alert.id_sitio = alerta.id_sitio
        alert.tipo_alertas = alerta.tipo_alertas
        alert.canal = alerta.canal
        alert.timestamp = alerta.timestamp
        self.db.commit()
        return

    def delete_alertas(self, id:int):
        self.db.query(AlertasModel).filter(AlertasModel.id == id).delete()
        self.db.commit()
        return
        
#     def delete_logeo(self, id: int):
#         self.db.query(LogModel).filter(LogModel.id == id).delete()
#         self.db.commit()
#         return 
    
