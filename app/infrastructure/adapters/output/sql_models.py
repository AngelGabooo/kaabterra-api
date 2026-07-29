# app/infrastructure/adapters/output/sql_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.infrastructure.config.database import Base

class SQLUsuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=True, default="Productor")
    acceptterms = Column(Boolean, nullable=False, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    farms = relationship("SQLFarm", back_populates="producer", cascade="all, delete-orphan")


class SQLFarm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(200), nullable=False)
    hectares = Column(Float, nullable=False, default=0.0)
    lots = Column(Integer, nullable=False, default=0)
    productivity = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="healthy")
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    altitude = Column(Integer, nullable=False, default=0)
    # ✅ Usar los nombres EXACTOS que agregaste en la base de datos
    establishmentYear = Column("establishmentYear", Integer, nullable=True)
    mainVariety = Column("mainVariety", String(100), nullable=True)
    productionSystem = Column("productionSystem", String(100), nullable=True)
    certifications = Column("certifications", JSON, nullable=True)
    producer_email = Column(String(150), ForeignKey("usuarios.email"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    producer = relationship("SQLUsuario", back_populates="farms")