from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.deps import get_db
from app.core.permissions import require_admin
from app.schemas.user import UserAdminResponse, UserAdminUpdate

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get(
    "/users",
    response_model=list[UserAdminResponse]
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users = db.query(User).all()
    return users

@router.get(
    "/users/{user_id}",
    response_model=UserAdminResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return user

@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if role not in ["user", "technician", "admin"]:
        raise HTTPException(
            status_code=400,
            detail="Role inválido"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    user.role = role
    db.commit()

    return {
        "message": f"Usuário {user.email} agora é {role}"
    }

@router.patch(
    "/users/{user_id}",
    response_model=UserAdminResponse
)
def update_user(
    user_id: int,
    user_in: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if user_in.name is not None:
        user.name = user_in.name

    if user_in.email is not None:
        user.email = user_in.email

    db.commit()
    db.refresh(user)

    return user

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admin não pode deletar a si mesmo"
        )

    db.delete(user)
    db.commit()
