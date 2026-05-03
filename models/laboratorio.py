from sqlalchemy import Column, Integer, String, Boolean
from database import Base
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("SCHEMA_NAME")


class Laboratorio(Base):
    __tablename__ = "laboratorios"
    __table_args__ = {"schema": SCHEMA}

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
