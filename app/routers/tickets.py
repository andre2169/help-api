from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse
from app.db.models.user import User
from app.core.dependencies import get_current_user
from app.deps import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cria um novo ticket para o usuário autenticado
    """

    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        user_id=current_user.id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def list_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista tickets do usuário autenticado
    """

    tickets = db.query(Ticket).filter(
        Ticket.user_id == current_user.id
    ).all()

    return tickets
