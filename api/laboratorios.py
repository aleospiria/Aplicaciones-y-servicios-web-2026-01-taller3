from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.laboratorio import LaboratorioCreate, LaboratorioResponse

router = APIRouter(prefix="/laboratorios", tags=["laboratorios"])


@router.post("/", response_model=LaboratorioResponse)
def crear_laboratorio(laboratorio: LaboratorioCreate, db: Session = Depends(get_db)):
    return crud.create_laboratorio(
        db=db,
        nombre=laboratorio.nombre,
        ubicacion=laboratorio.ubicacion,
        activo=laboratorio.activo
    )


@router.get("/", response_model=list[LaboratorioResponse])
def listar_laboratorios(db: Session = Depends(get_db)):
    return crud.get_all_laboratorios(db=db)


@router.get("/{id_laboratorio}", response_model=LaboratorioResponse)
def obtener_laboratorio(id_laboratorio: int, db: Session = Depends(get_db)):
    laboratorio = crud.get_laboratorio_by_id(db, id_laboratorio=id_laboratorio)
    if not laboratorio:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return laboratorio
