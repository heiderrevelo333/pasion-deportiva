from pydantic import BaseModel
from datetime import date, time
from typing import Optional

# For Request (POST /reservas) [cite: 30]
class ReservaCreate(BaseModel):
    cancha_id: int
    fecha: date # e.g., "2025-11-15"
    hora_inicio: time # e.g., "17:00"
    hora_fin: time # e.g., "18:00"

# For Admin actions (PUT /reservas/{id}) [cite: 29]
class ReservaUpdateAdmin(BaseModel):
    # Only allow status change
    estado: str 

# For Response [cite: 32]
class Reserva(BaseModel):
    id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str # e.g., 'pendiente' [cite: 25]
    
    # Fields to show the related entities
    usuario_id: int
    cancha_id: int
    
    class Config:
        orm_mode = True