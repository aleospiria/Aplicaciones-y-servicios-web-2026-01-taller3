from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str  # solicitante, auxiliar, admin, etc.
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str  # Contraseña en texto plano para el registro


class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True
