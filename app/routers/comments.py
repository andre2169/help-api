from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.comment import Comment
from app.db.models.ticket import Ticket
from app.db.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse

from app.deps import get_db
from app.core.permissions import require_user

router = APIRouter(
    prefix="/tickets/{ticket_id}/comments",
    tags=["Comments"]
)


# --------------------------------------------------
# Criar comentário
# --------------------------------------------------
@router.post(
    "/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    ticket_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    if ticket.status == "closed":
        raise HTTPException(
            status_code=400,
            detail="Ticket encerrado não permite comentários"
        )

    # Usuário comum → só no próprio ticket
    if current_user.role == "user" and ticket.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode comentar neste ticket"
        )

    # Técnico → só se estiver atribuído
    if current_user.role == "technician" and ticket.technician_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Técnico não atribuído ao ticket"
        )

    comment = Comment(
        content=comment_in.content,
        user_id=current_user.id,
        ticket_id=ticket.id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment
