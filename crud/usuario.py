from sqlalchemy.orm import Session
from models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_usuario(db: Session, nombre: str, correo: str, password: str, rol: str, activo: bool = True):
    password_hash = pwd_context.hash(password)
    db_usuario = Usuario(
        nombre=nombre,
        correo=correo,
        password_hash=password_hash,
        rol=rol,
        activo=activo
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuario_by_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def get_usuario_by_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def get_all_usuarios(db: Session):
    return db.query(Usuario).all()
