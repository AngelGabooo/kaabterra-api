# app/infrastructure/config/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# ✅ Obtener la URL de la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Si no está definida, usar la de desarrollo local
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:root@localhost:5432/kaab_terra_db"
    logger.warning("⚠️ Usando base de datos local")

# ✅ Corregir el formato de la URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ✅ Asegurar que sslmode esté correcto
if "sslmode" not in DATABASE_URL.lower():
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

logger.info(f"🔗 Conectando a base de datos...")
logger.info(f"📊 URL: {DATABASE_URL[:50]}...")

# ✅ Crear el engine con opciones adicionales para Neon
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()