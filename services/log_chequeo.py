from models.sitios import Sitios as SitiosModel
from models.log_chequeo import Log_chequeo as LogModel
from schemas.log_chequeo import Log_chequeo
from fastapi import HTTPException
from models.usuarios import Usuarios as UsuariosModel



class LogService():
    def __init__(self, db) -> None:
       self.db = db
    
    def crear_logeo(self, logeo: Log_chequeo):
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == logeo.id_sitio).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")
        nuevolog = LogModel(**logeo.dict())
        self.db.add(nuevolog)
        self.db.commit()
        return nuevolog

    def get_logeo(self):
        result = self.db.query(LogModel).all()
        return result
    
    def get_log_id(self, id:int):
        result = self.db.query(LogModel).filter(LogModel.id == id).first()
        return result
    
    def update_logeo(self, id: int, data:Log_chequeo):
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == data.id_sitio).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio web no encontrado")
    
        log = self.db.query(LogModel).filter(LogModel.id == id).first()
        log.id_sitio = data.id_sitio
        log.estado = data.estado
        log.tiempo_respuesta = data.tiempo_respuesta
        log.timestamp = data.timestamp
        self.db.commit()
        return
    
    def delete_logeo(self, id: int):
        self.db.query(LogModel).filter(LogModel.id == id).delete()
        self.db.commit()
        return 
    