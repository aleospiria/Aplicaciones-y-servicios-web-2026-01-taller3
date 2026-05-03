from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.servicio import ServicioCreate, ServicioResponse

router = APIRouter(prefix="/servicios", tags=["servicios"])


@router.post("/", response_model=ServicioResponse)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    return crud.create_servicio(
        db=db,
        nombre=servicio.nombre,
        descripcion=servicio.descripcion,
        activo=servicio.activo
    )


@router.get("/", response_model=list[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return crud.get_all_servicios(db=db)


@router.get("/{id_servicio}", response_model=ServicioResponse)
def obtener_servicio(id_servicio: int, db: Session = Depends(get_db)):
    servicio = crud.get_servicio_by_id(db, id_servicio=id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio
