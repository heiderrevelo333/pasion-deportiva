# app/routers/reserva.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.reserva import Reserva, ReservaCreate, ReservaUpdateAdmin
from app.dependencies.database import get_db
from app.crud import reserva as crud_reserva
from typing import List

# Mock function for getting the current user (simplifies the example)
def get_current_user(user_id: int = 1, rol: str = "jugador"): # Mocking a logged-in user 
    return {"id": user_id, "rol": rol}

# Dependency for Admin role checking (as required by PUT route [cite: 12])
def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["rol"] != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado: solo para administradores.")
    return current_user

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

# POST /api/v1/reservas: Crea una reserva [cite: 29]
@router.post("/", response_model=Reserva, status_code=status.HTTP_201_CREATED)
def create_reserva_route(
    reserva: ReservaCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Creates a new reservation with 'pendiente' status. 
    Checks for conflicts before creation.
    """
    try:
        return crud_reserva.create_reserva(db=db, reserva=reserva, user_id=current_user["id"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# GET /api/v1/reservas/mis: Muestra reservas del usuario [cite: 29]
@router.get("/mis", response_model=List[Reserva])
def read_my_reservas(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieves all reservations made by the current logged-in user.
    """
    return crud_reserva.get_user_reservas(db=db, user_id=current_user["id"])


# PUT /api/v1/reservas/{id}: Aprueba o cancela una reserva (admin) [cite: 29]
@router.put("/{reserva_id}", response_model=Reserva)
def update_reserva_route(
    reserva_id: int,
    update_data: ReservaUpdateAdmin,
    db: Session = Depends(get_db),
    # Requires Admin role to approve/reject
    current_admin: dict = Depends(is_admin) 
):
    """
    Updates the status of a reservation (e.g., 'aprobada', 'cancelada'). 
    Only accessible by an Administrator.
    """
    return crud_reserva.update_reserva_status(db=db, reserva_id=reserva_id, update_data=update_data)


# DELETE /api/v1/reservas/{id}: Cancela una reserva (jugador) [cite: 29]
@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reserva_route(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancels a reservation. Only the owner (Jugador) can use this route.
    """
    crud_reserva.cancel_reserva(db=db, reserva_id=reserva_id, user_id=current_user["id"])
    return None # Return 204 No Content for a successful DELETE