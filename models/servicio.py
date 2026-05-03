from sqlalchemy import Column, Integer, String, Boolean
from database import Base
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("SCHEMA_NAME")


class Servicio(Base):
    __tablename__ = "servicios"
    __table_args__ = {"schema": SCHEMA}

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
