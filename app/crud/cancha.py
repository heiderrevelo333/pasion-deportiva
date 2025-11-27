# app/crud/cancha.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cancha import Cancha
from app.schemas.cancha import CanchaCreate
from typing import List, Optional

def get_cancha_by_id(db: Session, cancha_id: int):
    """
    Retrieves a single court by its ID.
    """
    return db.query(Cancha).filter(Cancha.id == cancha_id).first()

def get_all_canchas(
    db: Session, 
    tipo: Optional[str] = None, 
    ubicacion: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100
) -> List[Cancha]:
    """
    Retrieves a paginated list of available (activa=True) courts, applying filters.
    The query parameters handle the 'tipo' and 'ubicacion' filters. 
    """
    # 1. Start with filtering for active courts only ("disponibles" [cite: 29])
    query = db.query(Cancha).filter(Cancha.estado == True)
    
    # 2. Apply optional 'tipo' filter
    if tipo:
        # Use func.lower for case-insensitive comparison
        query = query.filter(func.lower(Cancha.tipo) == func.lower(tipo))
    
    # 3. Apply optional 'ubicacion' filter (using LIKE for partial match)
    if ubicacion:
        query = query.filter(func.lower(Cancha.ubicacion).like(f"%{ubicacion.lower()}%"))
        
    # 4. Apply pagination [cite: 40]
    return query.offset(skip).limit(limit).all()

# --- Admin-specific function (Implied management: gestionar canchas) ---
# This is a basic example for data seeding or admin UI.

def create_cancha(db: Session, cancha: CanchaCreate):
    db_cancha = Cancha(**cancha.model_dump(), estado=True)
    db.add(db_cancha)
    db.commit()
    db.refresh(db_cancha)
    return db_cancha