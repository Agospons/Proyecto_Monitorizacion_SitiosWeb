from database import Base
from sqlalchemy import Column, Integer, Enum,ForeignKey, TIME, FLOAT, TIMESTAMP
from sqlalchemy.orm import relationship
from models.sitios import Sitios
from enum import Enum as PyEnum


class EstadoO_O(PyEnum):
    online = "online"
    offline = "offline"


class Log_chequeo(Base):

    __tablename__ = "log_chequeos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    id_sitio = Column(Integer, ForeignKey('sitios.id'))
    estado = Column(Enum(EstadoO_O))
    tiempo_respuesta = Column(FLOAT)
    timestamp = Column(TIME)

    sitios = relationship(Sitios)
