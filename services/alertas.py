from models.sitios import Sitios as SitiosModel
from models.alertas import Alertas as AlertasModel
from schemas.alertas import Alertas 
from fastapi import HTTPException
from datetime import date, datetime

class AlertasServices():
    def __init__(self, db) -> None:
       self.db = db
    
    def crear_alerta_automatica(self):

        ### crea alertas automatixamente con solo ver si esta el dominio vencido o el sistema caido (solo back)
        hoy = date.today()
        
        sitios_vencidos = self.db.query(SitiosModel).filter(
            SitiosModel.vencimiento_dominio <= hoy
        ).all()

        sitios_caidos = self.db.query(SitiosModel).filter(
            SitiosModel.estado == "offline"
        ).all()

        for sitio in sitios_vencidos:
            if sitios_vencidos:
                alerta = AlertasModel(
                    id_sitio = sitio.id,
                    tipo_alertas = "Vencimiento",
                    canal = "Sistema",
                    timestamp = datetime.now(),
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
                self.db.commit()

        for sitio in sitios_caidos:
            if sitios_caidos:
                alerta = AlertasModel(
                    id_sitio = sitio.id,
                    tipo_alertas = "Caida",
                    canal = "Sistema",
                    timestamp = datetime.now(),
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
                self.db.commit()
        return alerta
                

    def crear_alerta(self, alerta:Alertas): 
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == alerta.id_sitio).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")

        nueva_alerta = AlertasModel(**alerta.dict())
        self.db.add(nueva_alerta)
        self.db.commit()
        return nueva_alerta
    
        
    def get_alertas(self):
        try:
            return self.db.query(AlertasModel).order_by(AlertasModel.timestamp.desc()).all()
        except Exception as e:
            print(f"Error al obtener alertas: {e}")
            return []

    def get_alertas_hoy(self):
        hoy = date.today()
        try:
            return self.db.query(AlertasModel).filter(
                AlertasModel.fecha_alerta == hoy
            ).order_by(AlertasModel.timestamp.desc()).all()
        except Exception as e:
            print(f"Error al obtener alertas de hoy: {e}")
            return []
    
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
