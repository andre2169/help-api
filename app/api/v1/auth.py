from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.db.models.user import User

from app.services.auth_service import login_service
from app.core.exceptions import InvalidCredentials
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def _http_error(exc: Exception):
    if isinstance(exc, InvalidCredentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    raise exc


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        return login_service(
            db=db,
            email=data.email,
            password=data.password,
        )
    except Exception as e:
        _http_error(e)


@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
