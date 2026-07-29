# app/infrastructure/adapters/output/postgres_farm_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from app.infrastructure.adapters.output.sql_models import SQLFarm

logger = logging.getLogger(__name__)

class PostgresFarmRepositoryAdapter:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, name: str, location: str, hectares: float, lots: int,
               productivity: float, status: str, latitude: float,
               longitude: float, altitude: int, establishmentYear: Optional[int],
               mainVariety: Optional[str], productionSystem: Optional[str],
               certifications: Optional[List[str]], producerEmail: str):
        
        try:
            logger.info(f"📤 Creando finca: {name} para productor: {producerEmail}")
            sql_farm = SQLFarm(
                name=name,
                location=location,
                hectares=hectares,
                lots=lots,
                productivity=productivity,
                status=status,
                # ❌ imageUrl ELIMINADO
                latitude=latitude,
                longitude=longitude,
                altitude=altitude,
                establishmentYear=establishmentYear,
                mainVariety=mainVariety,
                productionSystem=productionSystem,
                certifications=certifications,
                producer_email=producerEmail,
            )
            self.db.add(sql_farm)
            self.db.commit()
            self.db.refresh(sql_farm)
            logger.info(f"✅ Finca creada con ID: {sql_farm.id}")
            return sql_farm
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error al crear finca: {e}")
            raise