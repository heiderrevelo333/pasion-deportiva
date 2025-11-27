# app/core/database.py (Revised)
import os
from dotenv import load_dotenv # <-- New import
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Load Environment Variables ---
# This looks for the .env file and loads its contents into environment variables
load_dotenv() 
# --- Configuration ---

# Now, we read the URL from the environment (either from .env or system environment)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file.")

# If the env contains mysql+mysqlclient but the mysqlclient driver is not available
# prefer the pure-Python pymysql driver which is easier to install on Windows.
if SQLALCHEMY_DATABASE_URL.startswith("mysql+mysqlclient"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "mysql+mysqlclient", "mysql+pymysql", 1
    )

# 1. Create the SQLAlchemy Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 2. Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base class for declarative models
Base = declarative_base()