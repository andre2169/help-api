from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)

    # open | in_progress | closed
    status = Column(String(20), nullable=False, default="open")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos

    # Usuário que criou o ticket
    owner = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="tickets"
    )

    # Usuário técnico atribuído ao ticket
    technician = relationship(
        "User",
        foreign_keys=[technician_id],
        back_populates="assigned_tickets"
    )

    # Comentários do ticket
    comments = relationship(
        "Comment",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )
   
    # Se apagar um ticket o evento some
    events = relationship(
       "TicketEvent",
       back_populates="ticket",
       cascade="all, delete-orphan"
    )