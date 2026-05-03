from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SCHEMA = os.getenv("SCHEMA_NAME")


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {"schema": SCHEMA}

    id_ticket = Column(Integer, primary_key=True, index=True)
    id_solicitante = Column(Integer, ForeignKey(f"{SCHEMA}.usuarios.id_usuario"), nullable=False)
    id_laboratorio = Column(Integer, ForeignKey(f"{SCHEMA}.laboratorios.id_laboratorio"), nullable=False)
    id_servicio = Column(Integer, ForeignKey(f"{SCHEMA}.servicios.id_servicio"), nullable=False)
    id_responsable = Column(Integer, ForeignKey(f"{SCHEMA}.usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey(f"{SCHEMA}.usuarios.id_usuario"), nullable=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="solicitado")  # solicitado, recibido, asignado, en_proceso, en_revision, terminado
    prioridad = Column(String, nullable=False, default="media")  # baja, media, alta
    observacion_responsable = Column(String, nullable=True)
    observacion_tecnico = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=True)

    # Relaciones
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante])
    responsable = relationship("Usuario", foreign_keys=[id_responsable])
    asignado = relationship("Usuario", foreign_keys=[id_asignado])
    laboratorio = relationship("Laboratorio")
    servicio = relationship("Servicio")
