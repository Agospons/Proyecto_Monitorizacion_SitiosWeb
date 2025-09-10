from database import Base
from sqlalchemy import Column, Integer, String, Enum, DATE

class Usuarios(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    nombre_completo = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    telefono = Column(Integer, nullable=False)
    observaciones = Column(String(100), nullable= True)
    fecha_alta = Column(DATE)
    password = Column(String(1000))


    # paquete_id = Column(Integer, ForeignKey('paquetes.id'), nullable=False)
    # usuario = relationship(Usuarios)
    # paquete = relationship(Paquetes)
