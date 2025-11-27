from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cancha(Base):
    __tablename__ = "canchas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True) 
    tipo = Column(String(50)) # e.g., 'fútbol', 'baloncesto' [cite: 23]
    ubicacion = Column(String(100)) 
    estado = Column(Boolean, default=True) # 'activa' (True) / 'inactiva' (False) [cite: 23]

    # Relationship to Reserva model 
    reservas = relationship("Reserva", back_populates="cancha")