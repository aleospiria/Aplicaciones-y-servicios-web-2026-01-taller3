from datetime import datetime, timedelta, timezone
import os
from jose import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from security.scopes import get_scopes_for_role

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if SECRET_KEY is None:
    raise RuntimeError("Falta configurar SECRET_KEY en el archivo .env")

# Hash de contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Crea un token JWT con los datos proporcionados."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = data.copy()
    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    """Obtiene el usuario actual a partir del token JWT."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if correo is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter(Usuario.correo == correo).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not user.activo:
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    return user


def require_scopes(*required_scopes: str):
    """
    Dependencia que verifica que el usuario tenga los scopes requeridos.
    Uso: @router.get("/", dependencies=[Depends(require_scopes("tickets:crear"))])
    """
    def dependency(user: Usuario = Depends(get_current_user)):
        user_scopes = get_scopes_for_role(user.rol)
        missing_scopes = set(required_scopes) - user_scopes

        if missing_scopes:
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para realizar esta acción",
            )

        return user

    return dependency
