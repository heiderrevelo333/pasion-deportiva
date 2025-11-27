# scripts/init_db.py
"""
Create the MySQL database (if missing) and run SQLAlchemy `create_all` to create tables.
Run with the project's virtualenv activated:

& ".venv\Scripts\Activate.ps1"
& ".venv\Scripts\python.exe" scripts\init_db.py

This script reads `DATABASE_URL` from the environment (or `./.env`).
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set. Check your .env file.")
    sys.exit(1)

try:
    url = make_url(DATABASE_URL)
except Exception as e:
    print("ERROR: could not parse DATABASE_URL:", e)
    sys.exit(1)

db_name = url.database
if not db_name:
    print("ERROR: DATABASE_URL does not contain a database name.")
    sys.exit(1)

# Build server URL without database (so we can create the DB)
drivername = url.drivername
username = url.username or ""
password = url.password or ""
host = url.host or "127.0.0.1"
port = url.port or 3306

# drivername may include +pymysql (e.g., mysql+pymysql)
server_url = f"{drivername}://"
if username:
    server_url += username
    if password:
        server_url += f":{password}"
server_url += f"@{host}:{port}/"

print(f"Connecting to server to ensure database '{db_name}' exists...")
try:
    engine = create_engine(server_url, echo=False)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
    print("Database ensured.")
except Exception as e:
    print("ERROR: could not create database:", repr(e))
    sys.exit(1)

# Now import the app's Base and models and create tables using the app's engine
try:
    from app.core.database import engine as app_engine, Base
    # Import models so they are registered on Base.metadata
    import app.models
except Exception as e:
    print("ERROR: could not import application models:", repr(e))
    sys.exit(1)

try:
    print("Creating tables...")
    Base.metadata.create_all(bind=app_engine)
    print("Tables created successfully (if they did not exist).")
except Exception as e:
    print("ERROR: could not create tables:", repr(e))
    sys.exit(1)
