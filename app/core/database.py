# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Configuration (Should be loaded from app/core/config.py or .env) ---
# Assuming a MySQL connection string based on the project's technology stack 
# NOTE: Replace the details below with your actual MySQL credentials
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3306/playtime_db"

# 1. Create the SQLAlchemy Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 2. Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base class for declarative models
Base = declarative_base()