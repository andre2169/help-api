from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse
from app.db.models.user import User
from app.deps import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Cria um novo chamado (ticket) para um usuário
    """

    # Verifica se o usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        user_id=user_id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("/", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    """
    Lista todos os tickets
    """
    tickets = db.query(Ticket).all()
    return tickets
