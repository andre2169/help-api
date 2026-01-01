from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password
from app.deps import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
   

    user_exists = db.query(User).filter(
        User.email == user_in.email
    ).first()

    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
