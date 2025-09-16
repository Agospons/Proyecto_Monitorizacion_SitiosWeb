from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Time, String, Enum
from sqlalchemy.orm import relationship
from models.sitios import Sitios
from enum import Enum as PyEnum

class TipoAlerta(PyEnum):
    caida = "Caida"
    vencimiento = "Vencimiento"

class Alertas(Base):

    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    id_sitio = Column(Integer, ForeignKey('sitios.id'), nullable=False)
    timestamp = Column(Time, nullable=False)
    tipo_alertas = Column(Enum(TipoAlerta))
    canal = Column(String(30), nullable=False)

    sitios = relationship(Sitios)

