from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.ticket import TicketCreate, TicketUpdate, TicketUpdateEstado, TicketResponse
from security.auth import get_current_user, require_scopes
from security.scopes import get_scopes_for_role
from models.usuario import Usuario

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Tabla de transiciones permitidas
TRANSICIONES_PERMITIDAS = {
   ("solicitado", "recibido"): {"scopes": {"tickets:recibir"}},
   ("recibido", "asignado"): {"scopes": {"tickets:asignar"}},
   ("asignado", "en_proceso"): {"scopes": {"tickets:atender"}, "requiere_asignado": True},
   ("en_proceso", "en_revision"): {"scopes": {"tickets:atender"}, "requiere_asignado": True},
   ("en_revision", "terminado"): {"scopes": {"tickets:finalizar"}},
}




def validar_transicion(estado_actual: str, estado_nuevo: str, user: Usuario):
   """Valida si la transición de estado está permitida."""
   clave = (estado_actual, estado_nuevo)
  
   if clave not in TRANSICIONES_PERMITIDAS:
       raise HTTPException(
           status_code=422,
           detail=f"Transición no permitida: de '{estado_actual}' a '{estado_nuevo}'"
       )
  
   reglas = TRANSICIONES_PERMITIDAS[clave]
  
   # Verificar si requiere ser el técnico asignado
   if reglas.get("requiere_asignado"):
       pass
  
   return reglas




@router.post("/", response_model=TicketResponse)
def crear_ticket(
   ticket: TicketCreate,
   db: Session = Depends(get_db),
   user: Usuario = Depends(require_scopes("tickets:crear"))
):
   # Verificar que el solicitante existe y es el usuario autenticado (o es admin)
   solicitante = crud.get_usuario_by_id(db, ticket.id_solicitante)
   if not solicitante:
       raise HTTPException(status_code=404, detail="Solicitante no encontrado")
  
   # Un usuario solo puede crear tickets para sí mismo (a menos que sea admin)
   if user.rol != "admin" and user.id_usuario != ticket.id_solicitante:
       raise HTTPException(
           status_code=403,
           detail="Solo puede crear tickets para usted mismo"
       )


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
def listar_tickets(
   db: Session = Depends(get_db),
   user: Usuario = Depends(get_current_user)
):
   """
   Lista tickets según el rol:
   - Admin: ve todos los tickets
   - Otros roles: ven solo tickets donde participan
   """
   if "tickets:ver_todos" in get_scopes_for_role(user.rol):
       # Admin ve todos
       return crud.get_all_tickets(db=db)
   else:
       # Usuarios normales ven solo los suyos
       tickets = crud.get_all_tickets(db=db)
       mis_tickets = [
           t for t in tickets
           if t.id_solicitante == user.id_usuario
           or t.id_responsable == user.id_usuario
           or t.id_asignado == user.id_usuario
       ]
       return mis_tickets




@router.get("/{id_ticket}", response_model=TicketResponse)
def obtener_ticket(
   id_ticket: int,
   db: Session = Depends(get_db),
   user: Usuario = Depends(get_current_user)
):
   """
   Obtiene un ticket específico si el usuario tiene permiso de verlo.
   """
   ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
   if not ticket:
       raise HTTPException(status_code=404, detail="Ticket no encontrado")
  
   # Admin puede ver todos
   if user.rol == "admin":
       return ticket
  
   # Otros solo pueden ver tickets donde participan
   if (ticket.id_solicitante != user.id_usuario and
       ticket.id_responsable != user.id_usuario and
       ticket.id_asignado != user.id_usuario):
       raise HTTPException(
           status_code=403,
           detail="No tiene permiso para ver este ticket"
       )
  
   return ticket




@router.patch("/{id_ticket}/estado", response_model=TicketResponse)
def actualizar_estado_ticket(
   id_ticket: int,
   estado_data: TicketUpdateEstado,
   db: Session = Depends(get_db),
   user: Usuario = Depends(get_current_user)
):
   """
   Actualiza el estado de un ticket validando:
   1. Que la transición esté permitida
   2. Que el usuario tenga el scope requerido
   3. Que el usuario sea el técnico asignado (si aplica)
   """
   ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
   if not ticket:
       raise HTTPException(status_code=404, detail="Ticket no encontrado")
  
   # Validar transición
   transicion = validar_transicion(ticket.estado, estado_data.estado, user)


   # Verificar scopes
   user_scopes = get_scopes_for_role(user.rol)
   if not transicion["scopes"].issubset(user_scopes):
       raise HTTPException(
           status_code=403,
           detail=f"No tiene el scope requerido para esta transición"
       )
  
   # Verificar si requiere ser el técnico asignado
   if transicion.get("requiere_asignado"):
       if user.rol != "admin" and ticket.id_asignado != user.id_usuario:
           raise HTTPException(
               status_code=403,
               detail="Solo el técnico asignado puede cambiar el estado de este ticket"
           )
  
   return crud.update_ticket_estado(
       db=db,
       id_ticket=id_ticket,
       estado=estado_data.estado,
       observacion_responsable=estado_data.observacion_responsable,
       observacion_tecnico=estado_data.observacion_tecnico
   )




@router.patch("/{id_ticket}", response_model=TicketResponse)
def actualizar_ticket(
   id_ticket: int,
   ticket_data: TicketUpdate,
   db: Session = Depends(get_db),
   user: Usuario = Depends(get_current_user)
):
   """
   Actualiza campos de un ticket (no el estado).
   Solo el solicitante o admin pueden modificar.
   """
   ticket = crud.get_ticket_by_id(db, id_ticket=id_ticket)
   if not ticket:
       raise HTTPException(status_code=404, detail="Ticket no encontrado")
  
   # Solo el solicitante o admin pueden modificar
   if user.rol != "admin" and ticket.id_solicitante != user.id_usuario:
       raise HTTPException(
           status_code=403,
           detail="Solo el solicitante puede modificar este ticket"
       )
  
   return crud.update_ticket(
       db=db,
       id_ticket=id_ticket,
       **ticket_data.model_dump(exclude_unset=True)
   )
