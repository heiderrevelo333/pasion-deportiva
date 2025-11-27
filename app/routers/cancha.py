# app/routers/cancha.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.cancha import Cancha
from app.dependencies.database import get_db
from app.crud import cancha as crud_cancha
from typing import List, Optional

router = APIRouter(
    prefix="/canchas",
    tags=["Canchas"]
)

# GET /api/v1/canchas: Lista canchas disponibles (filtros: tipo, ubicación). [cite: 29]
@router.get("/", response_model=List[Cancha], status_code=status.HTTP_200_OK)
def list_canchas_route(
    db: Session = Depends(get_db), 
    # Filters
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de cancha (e.g., fútbol, baloncesto)."),
    ubicacion: Optional[str] = Query(None, description="Filtrar por ubicación o parte de la ubicación."),
    # Pagination
    page: int = Query(1, ge=1, description="Número de página."),
    limit: int = Query(10, ge=1, le=100, description="Resultados por página.")
):
    """
    Retrieves a paginated list of available courts, with optional filters for type and location.
    The 'page' and 'limit' parameters implement the pagination requirement. [cite: 40]
    """
    skip = (page - 1) * limit
    canchas = crud_cancha.get_all_canchas(
        db=db, 
        tipo=tipo, 
        ubicacion=ubicacion, 
        skip=skip, 
        limit=limit
    )
    return canchas

# GET /api/v1/canchas/{id}: Muestra detalles de una cancha. [cite: 29]
@router.get("/{cancha_id}", response_model=Cancha, status_code=status.HTTP_200_OK)
def get_cancha_details_route(
    cancha_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieves detailed information for a specific court.
    """
    db_cancha = crud_cancha.get_cancha_by_id(db, cancha_id=cancha_id)
    if db_cancha is None:
        # Use the specified 404 error code for 'cancha no encontrada' [cite: 41]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cancha no encontrada."
        )
    return db_cancha