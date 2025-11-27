# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.usuario import Usuario, UsuarioCreate, UserLogin
from app.crud import usuario as crud_usuario

# --- Simple Authentication Logic (Mocked) ---
# NOTE: In a production app, this would involve JWT tokens stored in cookies/headers.
# For simplicity and "Login básico", we use a simple dependency mock here.

router = APIRouter(
    tags=["Auth & Usuarios"]
)

# Mock user data store for session simulation (replace with proper session/JWT logic)
MOCK_LOGGED_IN_USER_ID = 1

def get_current_user_mock(db: Session = Depends(get_db)):
    """
    MOCK Dependency: Simulates retrieving the currently logged-in user.
    In a real app, this would decode a JWT or check a session ID.
    """
    user = crud_usuario.get_user_by_id(db, MOCK_LOGGED_IN_USER_ID)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    return user

# The 'is_admin' dependency from reserva.py is already sufficient:
# from app.routers.reserva import is_admin 

# --- Endpoints ---

@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint for a new player (Jugador) to register.
    """
    return crud_usuario.create_user(db=db, user=user, rol="jugador")

@router.post("/login")
def login_for_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and simulates the login success.
    """
    user = crud_usuario.get_user_by_email(db, user_data.email)
    
    # 1. Check if user exists and password is correct
    if not user or not crud_usuario.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrecta"
        )
    
    # 2. Mocking successful login: return the user object (in a real app, you'd return a JWT)
    # The MOCK_LOGGED_IN_USER_ID above would be set here in a real session/JWT implementation.
    return {"message": "Login exitoso", "user_id": user.id, "rol": user.rol}

@router.get("/users/me", response_model=Usuario)
def read_users_me(current_user: Usuario = Depends(get_current_user_mock)):
    """
    Retrieves the details of the currently authenticated user (Jugador or Administrador).
    """
    return current_user