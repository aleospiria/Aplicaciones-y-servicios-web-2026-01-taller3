from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.usuario import UsuarioCreate, UsuarioResponse
from security.auth import require_scopes

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioResponse, dependencies=[Depends(require_scopes("usuarios:gestionar"))])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya existe
    existente = crud.get_usuario_by_correo(db, correo=usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    return crud.create_usuario(
        db=db,
        nombre=usuario.nombre,
        correo=usuario.correo,
        password=usuario.password,
        rol=usuario.rol,
        activo=usuario.activo
    )


@router.get("/", response_model=list[UsuarioResponse], dependencies=[Depends(require_scopes("usuarios:gestionar"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.get_all_usuarios(db=db)


@router.get("/{id_usuario}", response_model=UsuarioResponse, dependencies=[Depends(require_scopes("usuarios:gestionar"))])
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_id(db, id_usuario=id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
