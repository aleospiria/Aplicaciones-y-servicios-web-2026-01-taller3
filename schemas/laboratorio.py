from pydantic import BaseModel


class LaboratorioBase(BaseModel):
    nombre: str
    ubicacion: str
    activo: bool = True


class LaboratorioCreate(LaboratorioBase):
    pass


class LaboratorioResponse(LaboratorioBase):
    id_laboratorio: int

    class Config:
        from_attributes = True
