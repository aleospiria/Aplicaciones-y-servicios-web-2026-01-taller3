from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.ticket import TicketCreate, TicketUpdate, TicketUpdateEstado, TicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse)
def crear_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # Verificar que el solicitante existe
    solicitante = crud.get_usuario_by_id(db, ticket.id_solicitante)
    if not solicitante:
        raise HTTPException(status_code=404, detail="Solicitante no encontrado")
    
    # Verificar que el laboratorio existe
    laboratorio = crud.get_laboratorio_by_id(db, ticket.id_laboratorio)
    if not laboratorio:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    
    # Verificar que el servicio existe
    servicio = crud.get_servicio_by_id(db, ticket.id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return crud.create_ticket(
        db=db,
        titulo=ticket.titulo,
        descripcion=ticket.descripcion,
        id_solicitante=ticket.id_solicitante,
        id_laboratorio=ticket.id_laboratorio,
        id_servicio=ticket.id_servicio,
        prioridad=ticket.prioridad
    )


@router.get("/", response_model=list[TicketResponse])
def listar_tickets(db: Session = Depends(get_db)):
    return crud.get_all_tickets(db=db)


@router.get("/{id_ticket}", response_model=TicketResponse)
def obtener_ticket(id_ticket: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


@router.patch("/{id_ticket}/estado", response_model=TicketResponse)
def actualizar_estado_ticket(id_ticket: int, estado_data: TicketUpdateEstado, db: Session = Depends(get_db)):
    ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    return crud.update_ticket_estado(
        db=db,
        id_ticket=id_ticket,
        estado=estado_data.estado,
        observacion_responsable=estado_data.observacion_responsable,
        observacion_tecnico=estado_data.observacion_tecnico
    )


@router.patch("/{id_ticket}", response_model=TicketResponse)
def actualizar_ticket(id_ticket: int, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    return crud.update_ticket(
        db=db,
        id_ticket=id_ticket,
        **ticket_data.model_dump(exclude_unset=True)
    )
