from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import date

#activo, adherente, vitalicio, honorario, cadete 

class User(BaseModel):
    email: str
    password: str

class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: int
    observaciones: str
    fecha_alta: date

    class Config:
        from_attributes = True


class Usuarios(UsuarioBase):
    password: str = Field(min_length=8)


class UsuariosOut(BaseModel):
    id: int
    nombre_completo: str
    email: EmailStr
    telefono: int
    observaciones: str
    fecha_alta: date

    class Config:
        from_attributes = True


class UsuarioMini(BaseModel):
    nombre: str
    apellido: str

    class Config:
        from_attributes = True
