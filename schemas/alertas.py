from pydantic import BaseModel
from datetime import time, date
from enum import Enum

class TipoAlerta(str, Enum):
    caida = "Caida"
    vencimiento = "Vencimiento"

class Alertas(BaseModel):
    id_sitio: int
    tipo_alertas: TipoAlerta
    canal: str
    timestamp: time
    fecha_alerta: date

class alertasOut(BaseModel):
    id: int
    id_sitio: int
    tipo_alertas: TipoAlerta
    canal: str
    timestamp: time
    fecha_alerta: date
