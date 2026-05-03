from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.usuario import Usuario
from security.auth import verify_password, create_access_token, get_scopes_for_role

router = APIRouter(prefix="/auth", tags=["autenticación"])


class TokenRequest(BaseModel):
    correo: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    scopes: list[str]


@router.post("/token", response_model=TokenResponse)
def login(request: TokenRequest, db: Session = Depends(get_db)):
    """
    Inicio de sesión. Retorna un token JWT si las credenciales son válidas.
    """
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo == request.correo).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar contraseña
    if not verify_password(request.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar que esté activo
    if not usuario.activo:
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    # Crear token con los datos del usuario
    token_data = {
        "sub": usuario.correo,
        "id_usuario": usuario.id_usuario,
        "rol": usuario.rol,
    }

    access_token = create_access_token(token_data)
    scopes = list(get_scopes_for_role(usuario.rol))

    return TokenResponse(
        access_token=access_token,
        rol=usuario.rol,
        scopes=scopes
    )
