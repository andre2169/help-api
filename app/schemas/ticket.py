from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketBase(BaseModel):
    title: str
    description: str


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    status: str
    user_id: int
    technician_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
