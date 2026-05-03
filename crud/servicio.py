from sqlalchemy.orm import Session
from models.servicio import Servicio


def create_servicio(db: Session, nombre: str, descripcion: str, activo: bool = True):
    db_servicio = Servicio(
        nombre=nombre,
        descripcion=descripcion,
        activo=activo
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def get_servicio_by_id(db: Session, id_servicio: int):
    return db.query(Servicio).filter(Servicio.id_servicio == id_servicio).first()


def get_all_servicios(db: Session):
    return db.query(Servicio).all()
