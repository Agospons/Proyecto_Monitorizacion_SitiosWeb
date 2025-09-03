from database import Base
from sqlalchemy import Column, Integer, String, Enum

class Usuarios(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    telefono = Column(Integer, nullable=False)
    observaciones = Column(String(100))


    # paquete_id = Column(Integer, ForeignKey('paquetes.id'), nullable=False)
    # usuario = relationship(Usuarios)
    # paquete = relationship(Paquetes)
