from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    telefono: str
    email: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str # Field for creation, not exposed in the response

class Usuario(UsuarioBase):
    id: int
    rol: str
    is_active: bool

    class Config:
        # Allows Pydantic to read data directly from the SQLAlchemy model
        orm_mode = True
        
# app/schemas/usuario.py (Add this to the file)

class UserLogin(BaseModel):
    email: str
    password: str