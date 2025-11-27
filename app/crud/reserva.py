# app/crud/reserva.py
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate, ReservaUpdateAdmin
from datetime import date, time

# --- Helper function for overlap check ---

def check_for_overlap(db: Session, cancha_id: int, date: date, start_time: time, end_time: time, exclude_reserva_id: int = None):
    """
    Checks if a new reservation overlaps with any existing, approved, or pending one 
    on the same court and date.
    """
    # 1. Start time falls between existing reservation times:
    # (Existing.hora_inicio < New.hora_inicio < Existing.hora_fin)
    cond1 = and_(Reserva.hora_inicio < start_time, Reserva.hora_fin > start_time)
    
    # 2. End time falls between existing reservation times:
    # (Existing.hora_inicio < New.hora_fin < Existing.hora_fin)
    cond2 = and_(Reserva.hora_inicio < end_time, Reserva.hora_fin > end_time)
    
    # 3. New reservation completely envelops an existing one:
    # (New.hora_inicio <= Existing.hora_inicio AND New.hora_fin >= Existing.hora_fin)
    cond3 = and_(Reserva.hora_inicio >= start_time, Reserva.hora_fin <= end_time)

    # 4. Check for existing reservations that are 'pending' or 'aprobada'
    active_statuses = ["pendiente", "aprobada"]

    query = db.query(Reserva).filter(
        Reserva.cancha_id == cancha_id,
        Reserva.fecha == date,
        Reserva.estado.in_(active_statuses),
        or_(cond1, cond2, cond3)
    )

    if exclude_reserva_id:
        query = query.filter(Reserva.id != exclude_reserva_id)

    return query.first()

# --- CRUD Functions ---

def create_reserva(db: Session, reserva: ReservaCreate, user_id: int):
    # 1. Check for overlap before creating the reservation
    if check_for_overlap(db, reserva.cancha_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Horario ya reservado o solapado con una reserva existente." [cite: 41]
        )

    # 2. Create the Reserva object
    db_reserva = Reserva(
        **reserva.model_dump(),
        usuario_id=user_id,
        estado="pendiente"
    )
    
    # 3. Save to database
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def get_user_reservas(db: Session, user_id: int):
    # Get all reservations for the current user
    return db.query(Reserva).filter(Reserva.usuario_id == user_id).all() [cite: 29]

def get_reserva_by_id(db: Session, reserva_id: int):
    # Helper to fetch a single reservation
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()

def cancel_reserva(db: Session, reserva_id: int, user_id: int):
    db_reserva = get_reserva_by_id(db, reserva_id)

    if not db_reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")

    # 1. Check if the user owns the reservation or is an Admin (assuming admin check elsewhere)
    if db_reserva.usuario_id != user_id:
        # A proper admin check would be needed here, but for now, only the owner can cancel
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para cancelar esta reserva.")

    # 2. Update status
    db_reserva.estado = "cancelada"
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def update_reserva_status(db: Session, reserva_id: int, update_data: ReservaUpdateAdmin):
    # This function is used by the Admin (PUT /api/v1/reservas/{id}) [cite: 29]
    db_reserva = get_reserva_by_id(db, reserva_id)

    if not db_reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")

    # Apply new status
    db_reserva.estado = update_data.estado 
    
    # Optional: If the admin approves, you might want to re-run the overlap check just in case, 
    # but for simplicity, we assume the admin handles conflicts.
    
    db.commit()
    db.refresh(db_reserva)
    return db_reserva