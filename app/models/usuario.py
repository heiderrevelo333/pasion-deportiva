from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True) 
    telefono = Column(String(20), unique=True, index=True) # Sensitive/unique field [cite: 21, 27]
    rol = Column(String(20), default="jugador") # Values: 'jugador' or 'administrador' [cite: 21]

    # Added best practice fields for login/security
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    # Relationship to Reserva model 
    reservas = relationship("Reserva", back_populates="usuario")