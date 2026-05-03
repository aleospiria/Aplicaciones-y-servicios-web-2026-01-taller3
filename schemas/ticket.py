from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    titulo: str
    descripcion: str
    id_solicitante: int
    id_laboratorio: int
    id_servicio: int
    prioridad: str = Field(default="media", pattern="^(baja|media|alta)$")


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[str] = Field(None, pattern="^(baja|media|alta)$")
    id_asignado: Optional[int] = None
    id_responsable: Optional[int] = None
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None


class TicketUpdateEstado(BaseModel):
    estado: str = Field(..., pattern="^(solicitado|recibido|asignado|en_proceso|en_revision|terminado)$")
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None


class TicketResponse(TicketBase):
    id_ticket: int
    id_responsable: Optional[int] = None
    id_asignado: Optional[int] = None
    estado: str
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_finalizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
