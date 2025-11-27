from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    # This is where the actual DB insertion happens
    db_user = User(email=user.email, hashed_password=user.password) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user