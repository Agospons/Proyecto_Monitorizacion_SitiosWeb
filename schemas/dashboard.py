from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime, time
from enum import Enum


class Estadodominio(str, Enum):
    activo = "Activo"
    vencido = "Vencido"

class EstadoO_O(str, Enum):
    online = "online"
    offline = "offline"


class UsuariosResumen(BaseModel):
    id: int
    nombre_completo: str
    email: EmailStr
    telefono: int
    observaciones: str
    fecha_alta: date

class SitiosResumen(BaseModel):
    id: int
    dominio: str
    ip: str
    servidor: str
    id_cliente: int
    notas:str
    estado: EstadoO_O
    ultima_revision: datetime
    vencimiento_dominio: date
    estado_dominio: Estadodominio
    fecha_alta: date



class LogsResumen(BaseModel):
    id: int
    id_sitio: int
    estado: EstadoO_O
    tiempo_respuesta: Optional[float] = None
    timestamp: time

class TipoAlerta(str, Enum):
    caida = "Caida"
    vencimiento = "Vencimiento"

class AlertasResumen(BaseModel):
    id:int
    id_sitio: int
    tipo_alertas: TipoAlerta
    canal: str
    timestamp: time
    fecha_alerta: date

    

class DashboardStats(BaseModel):
    sitios_online: int
    sitios_offline: int
    dominio_vencido: int
    ultimos_usuarios: List[UsuariosResumen]
    
    web_no_online: List[SitiosResumen]
    alertas: List[AlertasResumen]
    
class Dash(BaseModel):
    historial_sitios: List[LogsResumen]

