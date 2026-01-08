from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse
from app.db.models.user import User
from app.services.timeline_service import get_ticket_timeline
from app.schemas.timeline import TimelineItem
from typing import List

from app.deps import get_db
from app.core.permissions import (
    require_user,
    require_technician,
)
from app.core.events import create_ticket_event

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

# --------------------------------------------------
# Criar ticket (USER)
# --------------------------------------------------
@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        user_id=current_user.id,
        status="open"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Evento: ticket criado
    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="CREATED",
        to_status="open",
    )

    db.commit()

    return ticket


# --------------------------------------------------
# Listar tickets
# USER → só os
# TECH/ADMIN → todos
# --------------------------------------------------
@router.get(
    "/",
    response_model=list[TicketResponse]
)
def list_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    if current_user.role in ["technician", "admin"]:
        return db.query(Ticket).all()

    tickets = db.query(Ticket).filter(
        Ticket.user_id == current_user.id
    ).all()
    return tickets
# --------------------------------------------------
# Técnico assume ticket
# open → in_progress
# --------------------------------------------------
@router.patch(
    "/{ticket_id}/assign",
    response_model=TicketResponse
)
def assign_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_technician),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    if ticket.status != "open":
        raise HTTPException(
            status_code=400,
            detail="Ticket não pode ser assumido"
        )

    old_status = ticket.status

    ticket.technician_id = current_user.id
    ticket.status = "in_progress"

    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="ASSIGNED",
        from_status=old_status,
        to_status="in_progress",
    )

    db.commit()
    db.refresh(ticket)

    return ticket


# --------------------------------------------------
# Técnico resolve ticket
# in_progress → resolved
# --------------------------------------------------
@router.patch(
    "/{ticket_id}/resolve",
    response_model=TicketResponse
)
def resolve_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_technician),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    if ticket.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail="Ticket não está em andamento"
        )

    old_status = ticket.status
    ticket.status = "resolved"

    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="RESOLVED",
        from_status=old_status,
        to_status="resolved",
    )

    db.commit()
    db.refresh(ticket)

    return ticket


# --------------------------------------------------
# Usuário confirma fechamento
# resolved → closed
# --------------------------------------------------
@router.patch(
    "/{ticket_id}/close",
    response_model=TicketResponse
)
def close_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    if ticket.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode fechar este ticket"
        )

    if ticket.status != "resolved":
        raise HTTPException(
            status_code=400,
            detail="Ticket ainda não foi resolvido"
        )

    old_status = ticket.status
    ticket.status = "closed"

    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="CLOSED",
        from_status=old_status,
        to_status="closed",
    )

    db.commit()
    db.refresh(ticket)

    return ticket




# --------------------------------------------------
# Time line do ticket
# --------------------------------------------------
def get_ticket_or_404(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )

    return ticket

@router.get(
    "/{ticket_id}/timeline",
    response_model=List[TimelineItem],
    response_model_exclude_none=True,
)
def ticket_timeline(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)

# ADMIN vê tudo
    if current_user.role == "admin":
        return get_ticket_timeline(db, ticket_id)

    # USUÁRIO dono do ticket
    if current_user.role == "user" and ticket.user_id == current_user.id:
        return get_ticket_timeline(db, ticket_id)

    # TÉCNICO responsável
    if current_user.role == "technician" and ticket.technician_id == current_user.id:
        return get_ticket_timeline(db, ticket_id)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Você não tem permissão para ver a timeline deste ticket"
    )