from sqlalchemy.orm import Session
from models.ticket import Ticket
from datetime import datetime


def create_ticket(db: Session, titulo: str, descripcion: str, id_solicitante: int,
                  id_laboratorio: int, id_servicio: int, prioridad: str = "media"):
    db_ticket = Ticket(
        titulo=titulo,
        descripcion=descripcion,
        id_solicitante=id_solicitante,
        id_laboratorio=id_laboratorio,
        id_servicio=id_servicio,
        prioridad=prioridad,
        estado="solicitado"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_ticket_by_id(db: Session, id_ticket: int):
    return db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def update_ticket_estado(db: Session, id_ticket: int, estado: str,
                         observacion_responsable: str = None,
                         observacion_tecnico: str = None):
    db_ticket = get_ticket_by_id(db, id_ticket)
    if db_ticket:
        db_ticket.estado = estado
        if observacion_responsable:
            db_ticket.observacion_responsable = observacion_responsable
        if observacion_tecnico:
            db_ticket.observacion_tecnico = observacion_tecnico
        if estado == "terminado":
            db_ticket.fecha_finalizacion = datetime.utcnow()
        db_ticket.fecha_actualizacion = datetime.utcnow()
        db.commit()
        db.refresh(db_ticket)
    return db_ticket


def update_ticket(db: Session, id_ticket: int, **kwargs):
    db_ticket = get_ticket_by_id(db, id_ticket)
    if db_ticket:
        for key, value in kwargs.items():
            if value is not None and hasattr(db_ticket, key):
                setattr(db_ticket, key, value)
        db_ticket.fecha_actualizacion = datetime.utcnow()
        db.commit()
        db.refresh(db_ticket)
    return db_ticket
