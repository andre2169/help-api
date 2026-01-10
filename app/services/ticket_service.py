from sqlalchemy.orm import Session
from app.db.models.ticket import Ticket
from app.core.events import create_ticket_event
from app.db.models.user import User
from app.core.exceptions import (
    TicketNotFound,
    TicketInvalidStatus,
    TicketPermissionDenied,
)


def _get_ticket_or_fail(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise TicketNotFound()
    return ticket


def create_ticket_service(*, db: Session, ticket_in, current_user: User) -> Ticket:
    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        user_id=current_user.id,
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="CREATED",
        to_status="open",
    )

    db.commit()
    return ticket


def assign_ticket_service(*, db: Session, ticket_id: int, current_user: User) -> Ticket:
    ticket = _get_ticket_or_fail(db, ticket_id)

    if ticket.status != "open":
        raise TicketInvalidStatus("Ticket não pode ser assumido")

    ticket.technician_id = current_user.id
    old_status = ticket.status
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


def resolve_ticket_service(*, db: Session, ticket_id: int, current_user: User) -> Ticket:
    ticket = _get_ticket_or_fail(db, ticket_id)

    if ticket.status != "in_progress":
        raise TicketInvalidStatus("Ticket não está em andamento")

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


def close_ticket_service(*, db: Session, ticket_id: int, current_user: User) -> Ticket:
    ticket = _get_ticket_or_fail(db, ticket_id)

    if ticket.user_id != current_user.id:
        raise TicketPermissionDenied("Você não pode fechar este ticket")

    if ticket.status != "resolved":
        raise TicketInvalidStatus("Ticket ainda não foi resolvido")

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


def list_tickets_service(*, db: Session, current_user: User):
    if current_user.role in ["technician", "admin"]:
        return db.query(Ticket).all()

    return db.query(Ticket).filter(Ticket.user_id == current_user.id).all()
