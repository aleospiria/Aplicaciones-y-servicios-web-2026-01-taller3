from sqlalchemy import Column, Integer, String, Boolean
from database import Base
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("SCHEMA_NAME")


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": SCHEMA}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # solicitante
    activo = Column(Boolean, default=True)
