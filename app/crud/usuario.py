# app/crud/usuario.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioBase

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Security Helpers ---

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# --- CRUD Functions ---

def get_user_by_email(db: Session, email: str):
    """Retrieves a user by their email address."""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Retrieves a user by their ID."""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db: Session, user: UsuarioCreate, rol: str = "jugador"):
    """
    Creates a new user, hashing their password before storing.
    Default role is 'jugador'.
    """
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Use the phone number as a unique/sensitive field 
    db_user = Usuario(
        nombre=user.nombre,
        telefono=user.telefono,
        email=user.email,
        hashed_password=hashed_password,
        rol=rol
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user