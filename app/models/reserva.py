from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date) 
    hora_inicio = Column(Time) 
    hora_fin = Column(Time) 
    estado = Column(String(20), default="pendiente") # 'pendiente', 'aprobada', 'cancelada' [cite: 25]

    # Foreign Keys [cite: 25]
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cancha_id = Column(Integer, ForeignKey("canchas.id"))

    # Relationships 
    usuario = relationship("Usuario", back_populates="reservas")
    cancha = relationship("Cancha", back_populates="reservas")
    
    # NOTE: The unique validation for overlapping times [cite: 27] will be handled in the CRUD logic.