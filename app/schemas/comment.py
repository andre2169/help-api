from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    ticket_id: int


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    ticket_id: int
    created_at: datetime

    class Config:
        from_attributes = True
