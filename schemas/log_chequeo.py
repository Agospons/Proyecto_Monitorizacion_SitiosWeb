from pydantic import BaseModel
from enum import Enum
from datetime import date, time


class EstadoO_O(str, Enum):
    online = "online"
    offline = "offline"

#LOGS_CHEQUEOS: id, sitio_id, estado, tiempo_respuesta, timestamp
class Log_chequeo(BaseModel):
    id_sitio: int
    estado: EstadoO_O
    tiempo_respuesta: float
    timestamp: time

    class Config:
        from_attributes = True
class logOut(BaseModel):
    id: int
    id_sitio: int
    estado: EstadoO_O
    tiempo_respuesta: float
    timestamp: time
    