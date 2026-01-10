from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.exceptions import UserAlreadyExists


def create_user_service(
    *,
    db: Session,
    user_in: UserCreate,
) -> User:
    user_exists = (
        db.query(User)
        .filter(User.email == user_in.email)
        .first()
    )

    if user_exists:
        raise UserAlreadyExists()

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
