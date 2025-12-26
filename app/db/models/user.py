from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # Segurança
    password_hash = Column(String, nullable=False)

    # user | technician | admin
    role = Column(String(20), default="user")

    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Tickets criados pelo usuário
    tickets = relationship(
        "Ticket",
        back_populates="owner",
        foreign_keys="Ticket.user_id"
    )

    # Tickets atribuídos como técnico
    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.technician_id"
    )

    # Comentários feitos pelo usuário
    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan"
    )
