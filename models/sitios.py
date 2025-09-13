from database import Base
from sqlalchemy import ForeignKey, Column, Integer, String, DATETIME, DATE, Enum, TIME
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.usuarios import Usuarios

class Estadodominio(PyEnum):
    activo = "Activo"
    vencido = "Vencido"

class EstadoO_O(PyEnum):
    online = "online"
    offline = "offline"



class Sitios(Base):
    __tablename__ = "sitios"

    id = Column(Integer, primary_key=True, index=True)
    dominio = Column(String(50), nullable=False)
    servidor = Column(String(50))
    ip = Column(String(20), unique=True)
    id_cliente = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    notas = Column(String(100))
    estado = Column(Enum(EstadoO_O))
    ultima_revision = Column(DATETIME)
    vencimiento_dominio = Column(DATE)
    estado_dominio = Column(Enum(Estadodominio))
    fecha_alta = Column(DATE)

    usuarios = relationship(Usuarios)
#
# SITIOS: id, dominio, ip, servidor, cliente_id, notas, estado, ultima_revision, vencimiento_dominio, estado_dominio, fecha_alta
