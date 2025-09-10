from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date

#SITIOS: id, dominio, ip, servidor, cliente_id, notas, estado, ultima_revision, 
#vencimiento_dominio, estado_dominio, fecha_alta

class Estadodominio(str, Enum):
    activo = "Activo"
    vencido = "Vencido"

class EstadoO_O(str, Enum):
    online = "online"
    offline = "offline"

class Sitios(BaseModel):
    dominio: str
    ip: int
    servidor: str
    id_cliente: int
    notas:str
    estado: EstadoO_O
    ultima_revision: datetime
    vencimiento_dominio: date
    estado_dominio: Estadodominio
    fecha_alta: date


class sitiosOut(BaseModel):
    id: int
    dominio: str
    ip: int
    servidor: str
    id_cliente: int
    notas:str
    estado: EstadoO_O
    ultima_revision: datetime
    vencimiento_dominio: date
    estado_dominio: Estadodominio
    fecha_alta: date

    class Config:
        from_attributes = True
