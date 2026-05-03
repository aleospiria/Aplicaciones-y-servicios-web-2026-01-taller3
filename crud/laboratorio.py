from sqlalchemy.orm import Session
from models.laboratorio import Laboratorio


def create_laboratorio(db: Session, nombre: str, ubicacion: str, activo: bool = True):
    db_laboratorio = Laboratorio(
        nombre=nombre,
        ubicacion=ubicacion,
        activo=activo
    )
    db.add(db_laboratorio)
    db.commit()
    db.refresh(db_laboratorio)
    return db_laboratorio


def get_laboratorio_by_id(db: Session, id_laboratorio: int):
    return db.query(Laboratorio).filter(Laboratorio.id_laboratorio == id_laboratorio).first()


def get_all_laboratorios(db: Session):
    return db.query(Laboratorio).all()
