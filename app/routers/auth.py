from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.security import verify_password
from app.db.models.user import User
from app.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
