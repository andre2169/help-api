from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "user"


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
