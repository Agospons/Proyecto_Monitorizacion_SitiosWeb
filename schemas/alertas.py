from pydantic import BaseModel
from datetime import time
from enum import Enum

class TipoAlerta(str, Enum):
    caida = "caida"
    vencimiento = "vencimiento"

class Alertas(BaseModel):
    id_sitio: int
    tipo_alertas: TipoAlerta
    canal: str
    timestamp: time

class alertasOut(BaseModel):
    id: int
    id_sitio: int
    tipo_alertas: TipoAlerta
    canal: str
    timestamp: time
