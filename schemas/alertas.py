from pydantic import BaseModel
from datetime import time


#ALERTAS: id, id_sitios, tipo_alerta, canal, timestamp.

class Alertas(BaseModel):
    id_sitio: int
    tipo_alertas: str
    canal: str
    timestamp: time

class alertasOut(BaseModel):
    id: int
    id_sitio: int
    tipo_alertas: str
    canal: str
    timestamp: time
