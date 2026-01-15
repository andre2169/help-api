from sqlalchemy.orm import Session

from app.db.models.user import User
from app.core.exceptions import (
    UserNotFound,
    InvalidUserRole,
    TicketPermissionDenied,
)


VALID_ROLES = ["user", "technician", "admin"]


def list_users_service(*, db: Session):
    return db.query(User).all()


def get_user_service(*, db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound("Usuário não encontrado")
    return user


def change_user_role_service(
    *,
    db: Session,
    user_id: int,
    role: str,
) -> User:
    if role not in VALID_ROLES:
        raise InvalidUserRole("Role inválido")

    user = get_user_service(db=db, user_id=user_id)

    user.role = role
    db.commit()
    db.refresh(user)

    return user


def update_user_service(
    *,
    db: Session,
    user_id: int,
    name: str | None,
    email: str | None,
) -> User:
    user = get_user_service(db=db, user_id=user_id)

    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

    db.commit()
    db.refresh(user)

    return user


def delete_user_service(
    *,
    db: Session,
    user_id: int,
    current_user: User,
):
    user = get_user_service(db=db, user_id=user_id)

    if user.id == current_user.id:
        raise TicketPermissionDenied(
            "Admin não pode deletar a si mesmo"
        )

    db.delete(user)
    db.commit()