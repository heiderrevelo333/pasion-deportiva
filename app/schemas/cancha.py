from pydantic import BaseModel
from typing import Optional

class CanchaBase(BaseModel):
    nombre: str
    tipo: str
    ubicacion: str

class CanchaCreate(CanchaBase):
    pass # No extra fields for creation

class Cancha(CanchaBase):
    id: int
    estado: bool # True for 'activa'

    class Config:
        orm_mode = True